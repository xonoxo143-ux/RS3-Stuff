#!/usr/bin/env python3
"""Detect unfinished Equilibrium tasks that look suspiciously close to completion.

This does not invent hidden in-game counters. Instead it looks for observable evidence:
- a direct level target is already satisfied or only a few levels away,
- a higher task in the same numbered family is already complete,
- an unfinished task is a gap between completed neighbours,
- a completed lower cumulative milestone establishes a useful lower bound,
- the task is in an activity/location cluster the account has already worked heavily.

Family and direct-completion signals use the task TITLE, not prerequisite text buried in
descriptions. Meeting a prerequisite is not the same thing as nearly finishing a task.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NON_ELITE_EXCLUSIONS = {"Invention"}


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


def task_title(task):
    return str(task.get("name", "")).strip()


def task_text(task):
    return f"{task.get('name', '')} {task.get('description', '')}".strip()


def number_signature(text):
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


def explicit_level_requirement(title):
    """Parse a direct single-skill achievement title."""
    low = title.lower().strip()
    if not re.match(r"^(reach|attain|get|have)\b", low):
        return None
    skills = [
        "Attack", "Defence", "Strength", "Constitution", "Ranged", "Prayer", "Magic",
        "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting",
        "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming",
        "Runecrafting", "Hunter", "Construction", "Summoning", "Dungeoneering",
        "Divination", "Invention", "Archaeology", "Necromancy",
    ]
    for skill in skills:
        s = re.escape(skill.lower())
        patterns = [
            rf"(?:reach|attain|get|have)\s+(?:at least\s+)?(?:level\s+)?(\d{{1,3}})\s+(?:(?:in|of)\s+(?:the\s+)?)?{s}\b",
            rf"(?:reach|attain|get|have)\s+{s}\s+(?:skill\s+)?(?:level\s+)?(\d{{1,3}})\b",
        ]
        vals = []
        for pattern in patterns:
            vals.extend(int(x) for x in re.findall(pattern, low, re.I))
        if vals:
            return skill, max(vals)
    return None


def all_skills_requirement(title, levels):
    """Evaluate titles like 'Reach at least level 50 in all non-elite skills'."""
    m = re.match(
        r"^reach\s+(?:at least\s+)?(?:level\s+)?(\d{1,3})\s+in\s+all\s+(non-elite\s+)?skills\b",
        title.lower().strip(),
    )
    if not m:
        return None
    required = int(m.group(1))
    non_elite = bool(m.group(2))
    eligible = {
        skill: int(level)
        for skill, level in levels.items()
        if not (non_elite and skill in NON_ELITE_EXCLUSIONS)
    }
    if not eligible:
        return None
    skill, current = min(eligible.items(), key=lambda kv: (kv[1], kv[0]))
    return {
        "required": required,
        "lowest_skill": skill,
        "lowest_level": current,
        "gap": max(0, required - current),
        "non_elite": non_elite,
    }


def accessible(task):
    return task.get("status") not in {"locked_region", "excluded", "known_issue"}


def effort_label(score, reasons, task):
    codes = {r["code"] for r in reasons}
    if "stated_requirement_already_met" in codes or "completed_harder_sibling" in codes:
        return "very_low_or_trigger_only"
    if "gap_between_completed_siblings" in codes:
        return "very_low"
    if "tiny_skill_gap" in codes or "all_skills_tiny_gap" in codes:
        gap = next((r.get("gap") for r in reasons if "gap" in r), None)
        return f"{gap}_skill_level{'s' if gap != 1 else ''}_or_less"
    if task.get("estimated_seconds") and int(task["estimated_seconds"]) <= 60:
        return "low"
    if score >= 65:
        return "probably_low"
    return "unknown_check_progress"


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
        template, nums = number_signature(task_title(task))
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
        title = task_title(task)
        low_title = title.lower()
        is_level_ladder = bool(re.match(r"^(reach|attain|get|have)\b", low_title))

        # Direct single-skill targets.
        req = explicit_level_requirement(title)
        if req:
            skill, required = req
            current = levels.get(skill, 0)
            gap = max(0, required - current)
            if gap == 0:
                score += 100
                confidence = max(confidence, 0.98)
                reasons.append({
                    "code": "stated_requirement_already_met",
                    "detail": f"Current {skill} is {current}, already at or above the task's {required} target.",
                    "skill": skill,
                    "current": current,
                    "required": required,
                })
            elif gap <= 2:
                score += 45
                confidence = max(confidence, 0.95)
                reasons.append({
                    "code": "tiny_skill_gap",
                    "detail": f"Only {gap} {skill} level(s) remain to the task target.",
                    "gap": gap,
                    "skill": skill,
                })
            elif gap <= 5:
                score += 25
                confidence = max(confidence, 0.9)
                reasons.append({
                    "code": "small_skill_gap",
                    "detail": f"Only {gap} {skill} levels remain to the task target.",
                    "gap": gap,
                    "skill": skill,
                })

        # Multi-skill threshold ladders are evaluated from actual current levels, not from
        # completion of easier milestones.
        all_req = all_skills_requirement(title, levels)
        if all_req:
            gap = all_req["gap"]
            if gap == 0:
                score += 100
                confidence = max(confidence, 0.98)
                reasons.append({
                    "code": "stated_requirement_already_met",
                    "detail": f"Lowest relevant skill is {all_req['lowest_skill']} {all_req['lowest_level']}, already meeting {all_req['required']}.",
                    **all_req,
                })
            elif gap <= 2:
                score += 45
                confidence = max(confidence, 0.95)
                reasons.append({
                    "code": "all_skills_tiny_gap",
                    "detail": f"Lowest relevant skill is {all_req['lowest_skill']} {all_req['lowest_level']}; only {gap} level(s) from the all-skills target.",
                    **all_req,
                })
            elif gap <= 5:
                score += 25
                confidence = max(confidence, 0.9)
                reasons.append({
                    "code": "all_skills_small_gap",
                    "detail": f"Lowest relevant skill is {all_req['lowest_skill']} {all_req['lowest_level']}; {gap} levels from the all-skills target.",
                    **all_req,
                })

        # Keep evaluator-known tiny skill blockers too, but avoid double-counting the same
        # skill task when the direct-title parser already handled it.
        blockers = task.get("blockers", []) or []
        skill_blockers = [b for b in blockers if b.get("type") == "skill"]
        other_blockers = [b for b in blockers if b.get("type") != "skill"]
        existing_gap_signal = any(r["code"] in {
            "tiny_skill_gap", "small_skill_gap", "all_skills_tiny_gap", "all_skills_small_gap"
        } for r in reasons)
        if not existing_gap_signal and len(skill_blockers) == 1 and not other_blockers:
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

        # Numeric families are useful for cumulative counters and sequences, but NOT for
        # level ladders, which were handled from actual levels above.
        fam = family_meta.get(tid)
        if fam and not is_level_ladder:
            template, nums = fam
            siblings = families.get(template, [])
            completed_sibs = [x for x in siblings if x in completed_ids]
            if completed_sibs:
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

                    if lower and target_num > 0:
                        best_lower = max(lower)
                        ratio = min(1.0, best_lower[0] / target_num)
                        # A completed cumulative milestone gives a guaranteed lower bound.
                        # It does NOT tell us the exact hidden counter.
                        if ratio >= 0.75:
                            add = 35
                            conf = 0.9
                        elif ratio >= 0.5:
                            add = 18
                            conf = 0.82
                        elif ratio >= 0.25:
                            add = 8
                            conf = 0.72
                        else:
                            add = 0
                            conf = 0.0
                        if add:
                            score += add
                            confidence = max(confidence, conf)
                            reasons.append({
                                "code": "family_progress_lower_bound",
                                "detail": f"Completed related milestone {best_lower[0]} proves at least {round(ratio * 100)}% of the {target_num} cumulative target was reached.",
                                "completed_task_id": best_lower[1],
                                "completed_value": best_lower[0],
                                "target_value": target_num,
                                "minimum_progress_fraction": round(ratio, 3),
                            })

                    # Small-number sequences (rooms, stages, tiers) are different from
                    # large cumulative counts. Immediate adjacency is strong evidence that
                    # the user may simply have stopped one step short.
                    nearest_distance = min(abs(n - target_num) for n, _ in comp_values)
                    if target_num <= 20 and nearest_distance == 1:
                        score += 40
                        confidence = max(confidence, 0.9)
                        reasons.append({
                            "code": "adjacent_completed_sibling",
                            "detail": "An immediately adjacent numbered task in the same sequence is complete.",
                        })

                ratio_family = len(completed_sibs) / max(1, len(siblings))
                if len(siblings) >= 3 and ratio_family >= 0.5 and any(
                    r["code"] in {
                        "family_progress_lower_bound", "completed_harder_sibling",
                        "gap_between_completed_siblings", "adjacent_completed_sibling"
                    } for r in reasons
                ):
                    score += round(12 * ratio_family)
                    confidence = max(confidence, 0.8)
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
            score += min(15, 3 + done)
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
            "tiny_skill_gap", "small_skill_gap",
            "all_skills_tiny_gap", "all_skills_small_gap",
            "completed_harder_sibling", "gap_between_completed_siblings",
            "adjacent_completed_sibling", "family_progress_lower_bound",
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
        "schema_version": 3,
        "purpose": "Surface forgotten or suspiciously near-complete unfinished tasks from observable account evidence.",
        "limitation": "WikiSync exposes completed task IDs and skill levels, not arbitrary hidden per-task counters. For cumulative families, completed milestones provide only a guaranteed lower bound; exact states such as 19/20 require a source that exposes that counter.",
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
        "> These are evidence-based suspects. Cumulative task families can establish a minimum progress floor, but exact hidden counters are not invented.",
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
