#!/usr/bin/env python3
"""Detect unfinished Equilibrium tasks that look suspiciously close to completion.

This does not invent hidden in-game counters. Instead it looks for observable evidence:
- the account already satisfies a stated skill threshold,
- a higher/equivalent task in the same numeric family is already complete,
- an unfinished task is a gap between completed neighbours,
- most siblings in the same task family are already complete,
- the task is in an activity/location cluster the account has already cleared heavily,
- the only known blocker is a tiny skill gap.

The output is deliberately separate from the normal speed ranking. It answers:
"What did I probably almost finish or forget to trigger?"
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name, default):
    try:
        return json.loads((ROOT / name).read_text(encoding="utf-8"))
    except Exception:
        return default


def dump(name, obj):
    (ROOT / name).write_text(
        json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def task_text(task):
    return f"{task.get('name', '')} {task.get('description', '')}".strip()


def number_signature(text):
    """Return a conservative numeric family template and explicit numbers.

    We only use numeric families when the surrounding wording is essentially identical.
    This is useful for room 1/2/3, kill 10/25/50, level 80/90/99, etc.
    """
    low = re.sub(r"\s+", " ", text.lower()).strip()
    nums = [int(x) for x in re.findall(r"(?<![a-z])\d{1,4}(?![a-z])", low)]
    if not nums:
        return None, []
    templ = re.sub(r"(?<![a-z])\d{1,4}(?![a-z])", "#", low)
    templ = re.sub(r"[^a-z#]+", " ", templ)
    templ = re.sub(r"\s+", " ", templ).strip()
    words = [w for w in templ.split() if w != "#"]
    if len(words) < 4:
        return None, nums
    return templ, nums


def explicit_level_requirement(text):
    """Parse common 'reach level N in Skill' wording without assuming every number is a level."""
    skills = [
        "Attack", "Defence", "Strength", "Constitution", "Ranged", "Prayer", "Magic",
        "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting",
        "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming",
        "Runecrafting", "Hunter", "Construction", "Summoning", "Dungeoneering",
        "Divination", "Invention", "Archaeology", "Necromancy",
    ]
    low = text.lower()
    for skill in skills:
        s = re.escape(skill.lower())
        patterns = [
            rf"(?:reach|attain|get|have)\s+(?:level\s+)?(\d{{1,3}})\s+(?:(?:in|of)\s+(?:the\s+)?)?{s}\b",
            rf"(?:level|at least)\s+(\d{{1,3}})\s+(?:(?:in|of)\s+(?:the\s+)?)?{s}\b",
            rf"\b{s}\s+(?:skill\s+)?(?:level\s+)?(\d{{1,3}})\b",
        ]
        vals = []
        for pattern in patterns:
            vals.extend(int(x) for x in re.findall(pattern, low, re.I))
        if vals:
            return skill, max(vals)
    return None


def accessible(task):
    return task.get("status") not in {
        "locked_region", "excluded", "known_issue"
    }


def effort_label(score, reasons, task):
    codes = {r["code"] for r in reasons}
    if "stated_requirement_already_met" in codes or "completed_harder_sibling" in codes:
        return "very_low_or_trigger_only"
    if "gap_between_completed_siblings" in codes:
        return "very_low"
    if "tiny_skill_gap" in codes:
        gap = next((r.get("gap") for r in reasons if r["code"] == "tiny_skill_gap"), None)
        return f"{gap}_skill_level{'s' if gap != 1 else ''}_or_less"
    if task.get("estimated_seconds") and int(task["estimated_seconds"]) <= 60:
        return "low"
    if score >= 65:
        return "probably_low"
    return "unknown"


def main():
    catalog = load("task-catalog.json", {}).get("tasks", [])
    summary = load("live-summary.json", {})
    unfinished_payload = load("live-unfinished.json", {})
    if isinstance(unfinished_payload, dict):
        unfinished = unfinished_payload.get("unfinished_tasks", [])
    elif isinstance(unfinished_payload, list):
        unfinished = unfinished_payload
    else:
        unfinished = []

    completed_ids = {int(x) for x in summary.get("completed_task_ids", [])}
    levels = {str(k): int(v) for k, v in summary.get("levels", {}).items()}
    by_id = {int(t["id"]): t for t in catalog if isinstance(t, dict) and "id" in t}
    unfinished_by_id = {int(t["id"]): t for t in unfinished if isinstance(t, dict) and "id" in t}

    families = collections.defaultdict(list)
    family_meta = {}
    for task in catalog:
        tid = int(task["id"])
        template, nums = number_signature(task_text(task))
        if template:
            families[template].append(tid)
            family_meta[tid] = (template, nums)

    cluster_unfinished = collections.Counter()
    for task in unfinished:
        if isinstance(task, dict) and accessible(task) and task.get("cluster"):
            cluster_unfinished[str(task["cluster"])] += 1

    cluster_patterns = {
        "sophanem_pyramid_plunder": r"pyramid plunder|sophanem",
        "lumbridge": r"lumbridge",
        "al_kharid": r"al kharid",
        "desert": r"desert|magic carpet|het'?s oasis|sophanem|menaphos|al kharid",
        "varrock": r"varrock|cooks?' guild",
        "fort_forinthry": r"fort forinthry|fort workshop",
        "karamja": r"karamja",
        "brimhaven": r"brimhaven",
        "havenhythe": r"havenhythe",
        "city_of_um": r"city of um|\bum\b",
    }
    cluster_completed = collections.Counter()
    for tid in completed_ids:
        task = by_id.get(tid)
        if not task:
            continue
        text = task_text(task)
        for cluster, pattern in cluster_patterns.items():
            if re.search(pattern, text, re.I):
                cluster_completed[cluster] += 1

    opportunities = []
    for tid, task in unfinished_by_id.items():
        if not accessible(task):
            continue
        reasons = []
        score = 0
        confidence = 0.0
        text = task_text(task)

        req = explicit_level_requirement(text)
        if req:
            skill, required = req
            current = levels.get(skill, 0)
            if current >= required:
                score += 100
                confidence = max(confidence, 0.98)
                reasons.append({
                    "code": "stated_requirement_already_met",
                    "detail": f"Current {skill} is {current}, already above the stated {required} requirement.",
                    "skill": skill,
                    "current": current,
                    "required": required,
                })

        blockers = task.get("blockers", []) or []
        skill_blockers = [b for b in blockers if b.get("type") == "skill"]
        other_blockers = [b for b in blockers if b.get("type") != "skill"]
        if len(skill_blockers) == 1 and not other_blockers:
            gap = int(skill_blockers[0].get("gap", 999))
            if gap <= 2:
                score += 45
                confidence = max(confidence, 0.95)
                reasons.append({
                    "code": "tiny_skill_gap",
                    "detail": f"Only known blocker is {gap} {skill_blockers[0]['skill']} level(s).",
                    "gap": gap,
                    "skill": skill_blockers[0]["skill"],
                })
            elif gap <= 5:
                score += 25
                confidence = max(confidence, 0.9)
                reasons.append({
                    "code": "small_skill_gap",
                    "detail": f"Only known blocker is {gap} {skill_blockers[0]['skill']} levels.",
                    "gap": gap,
                    "skill": skill_blockers[0]["skill"],
                })

        fam = family_meta.get(tid)
        if fam:
            template, nums = fam
            siblings = families.get(template, [])
            completed_sibs = [x for x in siblings if x in completed_ids]
            if completed_sibs:
                score += min(30, 8 * len(completed_sibs))
                confidence = max(confidence, 0.78)
                reasons.append({
                    "code": "same_task_family_progress",
                    "detail": f"{len(completed_sibs)} related task(s) in this numeric family are already complete.",
                    "completed_sibling_ids": completed_sibs[:20],
                })

                target_num = nums[0] if nums else None
                comp_values = []
                for sid in completed_sibs:
                    snums = family_meta.get(sid, (None, []))[1]
                    if snums:
                        comp_values.append((snums[0], sid))

                if target_num is not None and comp_values:
                    higher = [(n, sid) for n, sid in comp_values if n > target_num]
                    lower = [(n, sid) for n, sid in comp_values if n < target_num]
                    if higher:
                        nearest = min(higher)
                        score += 90
                        confidence = max(confidence, 0.96)
                        reasons.append({
                            "code": "completed_harder_sibling",
                            "detail": f"A higher-numbered related task ({nearest[0]}) is already complete while this {target_num} task is not.",
                            "completed_task_id": nearest[1],
                            "completed_value": nearest[0],
                            "target_value": target_num,
                        })
                    if lower and higher:
                        below = max(lower)
                        above = min(higher)
                        score += 85
                        confidence = max(confidence, 0.97)
                        reasons.append({
                            "code": "gap_between_completed_siblings",
                            "detail": f"This {target_num} task sits between completed related tasks {below[0]} and {above[0]}.",
                            "lower_task_id": below[1],
                            "upper_task_id": above[1],
                        })
                    nearest_distance = min(abs(n - target_num) for n, _ in comp_values)
                    if nearest_distance == 1:
                        score += 40
                        confidence = max(confidence, 0.9)
                        reasons.append({
                            "code": "adjacent_completed_sibling",
                            "detail": "An immediately adjacent numbered task in the same family is complete.",
                        })

                ratio = len(completed_sibs) / max(1, len(siblings))
                if len(siblings) >= 3 and ratio >= 0.5:
                    score += round(25 * ratio)
                    confidence = max(confidence, 0.85)
                    reasons.append({
                        "code": "family_mostly_complete",
                        "detail": f"{len(completed_sibs)}/{len(siblings)} tasks in this family are already complete.",
                        "completed": len(completed_sibs),
                        "total": len(siblings),
                    })

        cluster = task.get("cluster")
        if cluster and cluster_completed.get(cluster, 0) >= 3:
            done = cluster_completed[cluster]
            remain = cluster_unfinished.get(cluster, 0)
            score += min(20, 4 + done)
            confidence = max(confidence, 0.7)
            reasons.append({
                "code": "activity_cluster_already_worked",
                "detail": f"At least {done} completed tasks point to this same activity/location cluster.",
                "cluster": cluster,
                "completed_cluster_tasks": done,
                "known_unfinished_cluster_tasks": remain,
            })

        seconds = task.get("estimated_seconds")
        if reasons and seconds is not None:
            seconds = int(seconds)
            if seconds <= 30:
                score += 20
            elif seconds <= 60:
                score += 12
            elif seconds <= 120:
                score += 5

        substantive = {
            "stated_requirement_already_met",
            "tiny_skill_gap",
            "small_skill_gap",
            "same_task_family_progress",
            "completed_harder_sibling",
            "gap_between_completed_siblings",
            "adjacent_completed_sibling",
            "family_mostly_complete",
        }
        if not any(r["code"] in substantive for r in reasons):
            continue

        opportunities.append({
            "id": tid,
            "name": task.get("name"),
            "tier": task.get("tier"),
            "region": task.get("region"),
            "points": int(task.get("points") or 0),
            "status": task.get("status"),
            "cluster": cluster,
            "estimated_seconds_if_known": task.get("estimated_seconds"),
            "opportunity_score": score,
            "confidence": round(confidence, 2),
            "suspected_remaining_effort": effort_label(score, reasons, task),
            "reasons": reasons,
        })

    opportunities.sort(
        key=lambda x: (
            -x["opportunity_score"],
            -x["confidence"],
            x.get("estimated_seconds_if_known") if x.get("estimated_seconds_if_known") is not None else 999999,
            -x["points"],
            x["id"],
        )
    )

    result = {
        "schema_version": 1,
        "purpose": "Surface forgotten or suspiciously near-complete unfinished tasks from observable account evidence.",
        "limitation": "WikiSync exposes completed task IDs and skill levels, not arbitrary hidden per-task counters. Exact states such as 19/20 are only knowable if another live source exposes that counter.",
        "count": len(opportunities),
        "top": opportunities[:75],
        "signal_counts": dict(sorted(collections.Counter(
            r["code"] for o in opportunities for r in o["reasons"]
        ).items())),
    }
    dump("opportunities.json", result)

    assistant = load("assistant-state.json", {})
    assistant["forgotten_finish_opportunities"] = {
        "count": len(opportunities),
        "top": opportunities[:20],
        "source": "opportunities.json",
        "note": result["limitation"],
    }
    dump("assistant-state.json", assistant)

    section = ["", "## Forgotten-finish opportunities", ""]
    if opportunities:
        for o in opportunities[:12]:
            why = o["reasons"][0]["detail"] if o["reasons"] else "proximity signal"
            section.append(
                f"- [{o['id']}] **{o['name']}** — score {o['opportunity_score']}, "
                f"{o['suspected_remaining_effort']}; {why}"
            )
    else:
        section.append("- No strong automatic forgotten-finish signals right now.")
    section += [
        "",
        "> These are evidence-based suspects, not invented hidden counters. Exact 19/20-style progress requires a source that exposes that counter.",
    ]
    for filename in ["assistant-context.md", "report.md"]:
        path = ROOT / filename
        try:
            text = path.read_text(encoding="utf-8")
            marker = "\n## Forgotten-finish opportunities\n"
            if marker in text:
                text = text.split(marker, 1)[0].rstrip() + "\n"
            path.write_text(text.rstrip() + "\n" + "\n".join(section) + "\n", encoding="utf-8")
        except Exception:
            pass


if __name__ == "__main__":
    main()
