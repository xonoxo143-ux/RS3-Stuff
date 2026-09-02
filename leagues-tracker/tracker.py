#!/usr/bin/env python3
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from task_intelligence import merge_metadata, recommendation_metrics


def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def dump(path, obj):
    path.write_text(
        json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_iso(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def age_seconds(value, now_dt):
    stamp = parse_iso(value)
    if not stamp:
        return None
    return max(0, int((now_dt - stamp).total_seconds()))


def norm(o):
    return {
        "id": int(o["id"]),
        "name": str(o.get("name", "")).strip(),
        "description": str(o.get("description", "")).strip(),
        "tier": str(o.get("tier", "")).lower(),
        "region": str(o.get("region", "")).strip(),
        "points": int(o.get("points", 0)),
        "blessing_task": bool(o.get("blessingTask", o.get("blessing_task", False))),
        "issue": o.get("issue") or None,
    }


def parse_catalog(path):
    raw = path.read_text(encoding="utf-8")
    chunks = []
    rx = re.compile(r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)', re.S)
    for match in rx.finditer(raw):
        try:
            chunks.append(json.loads(match.group(1)))
        except Exception:
            pass

    decoded = "\n".join(chunks)
    decoder = json.JSONDecoder()
    pos = 0
    found = {}
    while True:
        pos = decoded.find('{"id":"', pos)
        if pos < 0:
            break
        try:
            obj, end = decoder.raw_decode(decoded[pos:])
        except Exception:
            pos += 1
            continue
        pos += max(end, 1)
        if isinstance(obj, dict) and {"id", "name", "tier", "region", "points"} <= set(obj):
            try:
                task = norm(obj)
                found[task["id"]] = task
            except Exception:
                pass
    return sorted(found.values(), key=lambda x: x["id"])


def catalog(now):
    cached = load(ROOT / "task-catalog.json", {})
    old = [norm(x) for x in cached.get("tasks", []) if isinstance(x, dict) and "id" in x]
    old_by_id = {x["id"]: x for x in old}
    tasks = old
    status = "cached"
    fetched = cached.get("fetched_at_utc")
    change = {
        "status": "not_checked",
        "added_task_ids": [],
        "removed_task_ids": [],
        "changed_task_ids": [],
        "previous_task_count": len(old),
        "current_task_count": len(old),
    }

    html = REPO / "task-catalog.html"
    if html.exists():
        try:
            fresh = parse_catalog(html)
            if len(fresh) >= 1100:
                fresh_by_id = {x["id"]: x for x in fresh}
                added = sorted(set(fresh_by_id) - set(old_by_id))
                removed = sorted(set(old_by_id) - set(fresh_by_id))
                changed = sorted(
                    tid
                    for tid in set(fresh_by_id) & set(old_by_id)
                    if fresh_by_id[tid] != old_by_id[tid]
                )
                tasks = fresh
                if added or removed or changed:
                    status = "fresh_updated"
                    fetched = now
                    change["status"] = "changed"
                else:
                    status = "fresh_unchanged"
                    change["status"] = "unchanged"
                change.update(
                    added_task_ids=added,
                    removed_task_ids=removed,
                    changed_task_ids=changed,
                    current_task_count=len(fresh),
                )
        except Exception as exc:
            change["status"] = "parse_failed"
            change["error"] = repr(exc)

    if len(tasks) < 1100:
        raise RuntimeError("No valid Equilibrium task catalog available")

    dump(
        ROOT / "task-catalog.json",
        {
            "schema_version": 2,
            "source": "ScapeLeagues Equilibrium task database",
            "source_url": "https://scapeleagues.com/rs3/equilibrium/tasks",
            "fetched_at_utc": fetched,
            "task_count": len(tasks),
            "tasks": tasks,
        },
    )
    return tasks, status, fetched, change


def relic_tier(rules, lp):
    tier = 0
    for key, value in sorted(rules["relics"]["tiers"].items(), key=lambda x: int(x[0])):
        if lp >= int(value["points"]):
            tier = int(key)
    return tier


def next_relic(rules, lp):
    for key, value in sorted(rules["relics"]["tiers"].items(), key=lambda x: int(x[0])):
        threshold = int(value["points"])
        if lp < threshold:
            return {
                "tier": int(key),
                "threshold": threshold,
                "remaining_points": threshold - lp,
            }
    return None


def next_region(rules, count):
    milestones = [
        {"id": "karamja", "tasks": int(x["tasks"]), "region": x.get("region")}
        for x in rules["regions"].get("automatic", [])
    ]
    milestones += [
        {"id": x["id"], "tasks": int(x["tasks"]), "region": None}
        for x in rules["regions"].get("elective_thresholds", [])
    ]
    for milestone in sorted(milestones, key=lambda x: x["tasks"]):
        if count < milestone["tasks"]:
            return {
                **milestone,
                "remaining_tasks": milestone["tasks"] - count,
            }
    return None


def blessing_progress(rules, count):
    order = ["t1", "t2", "t3", "god1", "t4", "t5", "t6", "god2"]
    current = None
    nxt = None
    for key in order:
        threshold = int(rules["blessings"]["steps"][key]["tasks"])
        if count >= threshold:
            current = key
        elif nxt is None:
            nxt = {
                "step": key,
                "threshold": threshold,
                "remaining_tasks": threshold - count,
            }
    return current, nxt


def god_choice(values):
    values = [int(x) for x in values if x in (1, 2, 3)]
    if len(values) != 3:
        return None
    counts = collections.Counter(values)
    for path, n in counts.items():
        if n >= 2:
            return path
    return 2


def resolve_relics(rules, state, tier):
    vector = state.get("relic_choice_vector", [])
    selected = []
    passive = []
    for n in range(1, 8):
        tier_data = rules["relics"]["tiers"][str(n)]
        choice = vector[n - 1] if len(vector) >= n else None
        option = (
            tier_data.get("options", {}).get(str(choice))
            if choice is not None
            else None
        )
        selected.append(
            {
                "tier": n,
                "unlocked": n <= tier,
                "choice_number": choice,
                "name": option.get("name") if option else None,
                "effects": option.get("effects", []) if option else [],
                "threshold_points": int(tier_data["points"]),
                "xp_multiplier": int(tier_data["xp_multiplier"]),
            }
        )
        if n <= tier:
            passive.append(
                {
                    "tier": n,
                    "effects": tier_data.get("passive_effects", []),
                }
            )
    return selected, passive


def resolve_blessings(rules, state, count):
    vector = state.get("blessing_path_vector", {})
    gods = {
        "god1": god_choice([vector.get("t1"), vector.get("t2"), vector.get("t3")]),
        "god2": god_choice([vector.get("t4"), vector.get("t5"), vector.get("t6")]),
    }
    out = []
    passive = []
    active_path_values = []

    for key in ["t1", "t2", "t3", "god1", "t4", "t5", "t6", "god2"]:
        step = rules["blessings"]["steps"][key]
        unlocked = count >= int(step["tasks"])
        choice = gods.get(key) if key.startswith("god") else vector.get(key)
        option = step.get("options", {}).get(str(choice)) if choice is not None else None
        out.append(
            {
                "step": key,
                "unlocked": unlocked,
                "threshold_tasks": int(step["tasks"]),
                "choice_number": choice,
                "path": (
                    rules["blessings"]["path_encoding"].get(str(choice))
                    if choice
                    else None
                ),
                "name": option.get("name") if option else None,
                "effects": option.get("effects", []) if option else [],
                "derived": key.startswith("god"),
            }
        )
        if unlocked:
            passive.append(
                {
                    "step": key,
                    "effects": step.get("passive_effects", []),
                }
            )
            if not key.startswith("god") and choice in (1, 2, 3):
                active_path_values.append(int(choice))

    dynamic = []
    t4 = next((x for x in out if x["step"] == "t4"), None)
    unique = len(set(active_path_values))
    if t4 and t4["unlocked"] and t4["name"] == "True Equilibrium":
        dynamic = [
            {
                "source": "True Equilibrium",
                "unique_paths_currently_chosen": unique,
                "current_bonus": {
                    "base_ability_damage": 75 * unique,
                    "armour": 50 * unique,
                    "life_points": 500 * unique,
                    "critical_strike_chance_percent": 5 * unique,
                    "critical_strike_damage_percent": 7.5 * unique,
                    "prayer_bonus": 5 * unique,
                },
            }
        ]
    return out, passive, gods, dynamic


def evaluate(task, override, levels, regions, exclusions, flags):
    result = dict(task)
    tid = task["id"]
    result.update(
        {
            "estimated_seconds": None,
            "cluster": None,
            "tags": [],
            "items_to_prepare": [],
            "blockers": [],
            "unknown_checks": [],
            "metadata_source": "none",
            "confidence": 0.0,
        }
    )

    if tid in exclusions:
        result.update(
            status="excluded",
            exclusion_reason=exclusions[tid],
        )
        result.update(recommendation_metrics(result))
        return result

    if task.get("issue"):
        result.update(
            status="known_issue",
            blockers=[{"type": "issue", "detail": task["issue"]}],
        )
        result.update(recommendation_metrics(result))
        return result

    if task.get("region") != "Global" and task.get("region") not in regions:
        result.update(
            status="locked_region",
            blockers=[{"type": "region", "required": task.get("region")}],
        )
        result.update(recommendation_metrics(result))
        return result

    meta = merge_metadata(task, override)
    blockers = []
    unknown = []

    required_region = meta.get("region")
    if required_region and required_region != "Global" and required_region not in regions:
        blockers.append({"type": "region", "required": required_region})

    for skill, required in (meta.get("skills") or {}).items():
        current = int(levels.get(skill, 0))
        if current < int(required):
            blockers.append(
                {
                    "type": "skill",
                    "skill": skill,
                    "required": int(required),
                    "current": current,
                    "gap": int(required) - current,
                }
            )

    for flag in meta.get("manual_requirements", []) or []:
        value = flags.get(flag)
        if value is False:
            blockers.append(
                {
                    "type": "manual_flag",
                    "flag": flag,
                    "required": True,
                    "current": False,
                }
            )
        elif value is not True:
            unknown.append(
                {
                    "type": "manual_flag",
                    "flag": flag,
                    "current": value,
                }
            )

    result.update(
        estimated_seconds=meta.get("estimated_seconds"),
        cluster=meta.get("cluster"),
        tags=meta.get("tags", []),
        items_to_prepare=meta.get("items", []),
        blockers=blockers,
        unknown_checks=unknown,
        metadata_source=meta.get("source", "none"),
        confidence=float(meta.get("confidence") or 0),
    )

    if blockers:
        result["status"] = "blocked"
    elif unknown:
        result["status"] = "manual_check"
    elif meta.get("source") == "manual_override":
        result["status"] = "verified_ready"
    elif meta.get("source") == "text_inference":
        result["status"] = "inferred_candidate"
    else:
        result["status"] = "accessible_requirements_unknown"

    result.update(recommendation_metrics(result))
    return result


def task_ref(task):
    return {
        "id": task["id"],
        "name": task["name"],
        "tier": task["tier"],
        "region": task["region"],
        "points": task["points"],
        "status": task.get("status"),
        "estimated_seconds": task.get("estimated_seconds"),
        "cluster": task.get("cluster"),
        "confidence": task.get("confidence"),
        "recommendation_grade": task.get("recommendation_grade"),
        "lp_per_minute": task.get("lp_per_minute"),
        "items_to_prepare": task.get("items_to_prepare", []),
        "blockers": task.get("blockers", []),
        "unknown_checks": task.get("unknown_checks", []),
    }


def recommendation_bundle(tasks, progression, state):
    verified = sorted(
        [
            t
            for t in tasks
            if t["status"] == "verified_ready" and t.get("estimated_seconds") is not None
        ],
        key=lambda t: (
            t.get("task_count_efficiency", 999999),
            t["estimated_seconds"],
            -t["points"],
            t["id"],
        ),
    )
    inferred = sorted(
        [
            t
            for t in tasks
            if t["status"] == "inferred_candidate"
            and t.get("estimated_seconds") is not None
        ],
        key=lambda t: (
            t.get("task_count_efficiency", 999999),
            t["estimated_seconds"],
            -t["points"],
            t["id"],
        ),
    )
    manual = sorted(
        [
            t
            for t in tasks
            if t["status"] == "manual_check" and t.get("estimated_seconds") is not None
        ],
        key=lambda t: (t["estimated_seconds"], -t["points"], t["id"]),
    )
    high_lp = sorted(
        verified + inferred,
        key=lambda t: (
            0 if t.get("recommendation_grade") == "A" else 1,
            -(t.get("lp_per_minute") or 0),
            t["estimated_seconds"],
            t["id"],
        ),
    )

    clusters = collections.defaultdict(list)
    for task in verified + inferred + manual:
        if task.get("cluster"):
            clusters[task["cluster"]].append(task)

    cluster_bundles = []
    for cluster, items in clusters.items():
        items = sorted(
            items,
            key=lambda t: (
                0 if t["status"] == "verified_ready" else 1,
                t.get("task_count_efficiency") or 999999,
                t["id"],
            ),
        )
        known_seconds = sum(int(t["estimated_seconds"]) for t in items if t.get("estimated_seconds"))
        cluster_bundles.append(
            {
                "cluster": cluster,
                "task_count": len(items),
                "verified_count": sum(t["status"] == "verified_ready" for t in items),
                "estimated_action_seconds": known_seconds,
                "points": sum(int(t["points"]) for t in items),
                "tasks": [task_ref(t) for t in items[:25]],
            }
        )
    cluster_bundles.sort(
        key=lambda x: (
            -x["verified_count"],
            -x["task_count"],
            x["estimated_action_seconds"],
            x["cluster"],
        )
    )

    next_region_data = progression.get("next_region") or {}
    needed = int(next_region_data.get("remaining_tasks") or 0)
    primary = verified[:needed] if needed else []
    missing = max(0, needed - len(primary))
    inferred_fill = inferred[:missing]
    sprint = primary + inferred_fill

    cluster_order = {"bank": 0, "anywhere": 1, "bank_or_range": 2}
    sprint = sorted(
        sprint,
        key=lambda t: (
            cluster_order.get(t.get("cluster"), 10),
            t.get("cluster") or "zzz",
            t["estimated_seconds"] or 999999,
            t["id"],
        ),
    )
    prep = []
    for task in sprint:
        for item in task.get("items_to_prepare", []):
            if item not in prep:
                prep.append(item)

    nearly_unblocked = []
    for task in tasks:
        if task.get("status") != "blocked":
            continue
        skill_blockers = [b for b in task.get("blockers", []) if b.get("type") == "skill"]
        other_blockers = [b for b in task.get("blockers", []) if b.get("type") != "skill"]
        if len(skill_blockers) == 1 and not other_blockers and skill_blockers[0].get("gap", 999) <= 5:
            nearly_unblocked.append(
                {
                    **task_ref(task),
                    "unlock": skill_blockers[0],
                }
            )
    nearly_unblocked.sort(key=lambda t: (t["unlock"]["gap"], t["unlock"]["skill"], t["id"]))

    source_counts = collections.Counter(t.get("metadata_source", "none") for t in tasks)
    status_counts = collections.Counter(t.get("status", "unknown") for t in tasks)

    return {
        "schema_version": 1,
        "goal": state.get("goal"),
        "next_region_target": next_region_data or None,
        "goal_sprint": {
            "tasks_needed": needed,
            "selected_count": len(sprint),
            "verified_count": sum(t["status"] == "verified_ready" for t in sprint),
            "inferred_count": sum(t["status"] == "inferred_candidate" for t in sprint),
            "estimated_action_seconds_excluding_travel": sum(
                int(t.get("estimated_seconds") or 0) for t in sprint
            ),
            "prep_list": prep,
            "tasks": [task_ref(t) for t in sprint],
            "note": (
                "Grade A tasks come from explicit tracker metadata. Grade B tasks are "
                "conservative text-inferred candidates and should be verified before relying on them."
            ),
        },
        "fastest_verified": [task_ref(t) for t in verified[:50]],
        "fastest_inferred_backups": [task_ref(t) for t in inferred[:50]],
        "manual_checks": [task_ref(t) for t in manual[:50]],
        "highest_lp_per_minute": [task_ref(t) for t in high_lp[:50]],
        "cluster_bundles": cluster_bundles[:50],
        "nearly_unblocked": nearly_unblocked[:50],
        "coverage": {
            "metadata_source_counts": dict(sorted(source_counts.items())),
            "status_counts": dict(sorted(status_counts.items())),
            "timed_verified_tasks": len(verified),
            "timed_inferred_candidates": len(inferred),
        },
    }


def validate_state(rules, state, task_count, relic_level, blessing_count, missing_catalog_ids):
    warnings = []
    errors = []

    elective_thresholds = rules["regions"].get("elective_thresholds", [])
    expected_elective_slots = sum(task_count >= int(x["tasks"]) for x in elective_thresholds)
    selected_elective = len(state.get("regions", {}).get("elective", []) or [])
    if selected_elective < expected_elective_slots:
        warnings.append(
            {
                "code": "elective_region_selection_due",
                "detail": (
                    f"{expected_elective_slots} elective region slot(s) are unlocked but only "
                    f"{selected_elective} are recorded."
                ),
            }
        )
    if selected_elective > expected_elective_slots:
        errors.append(
            {
                "code": "too_many_elective_regions",
                "detail": (
                    f"{selected_elective} elective regions recorded but only "
                    f"{expected_elective_slots} slot(s) are unlocked."
                ),
            }
        )

    automatic = state.get("regions", {}).get("automatic", []) or []
    for entry in rules["regions"].get("automatic", []):
        if task_count >= int(entry["tasks"]) and entry["region"] not in automatic:
            warnings.append(
                {
                    "code": "automatic_region_missing",
                    "detail": f"{entry['region']} should be unlocked at {entry['tasks']} tasks.",
                }
            )

    relic_vector = state.get("relic_choice_vector", [])
    for tier in range(1, relic_level + 1):
        value = relic_vector[tier - 1] if len(relic_vector) >= tier else None
        if value is None:
            warnings.append(
                {
                    "code": "unrecorded_relic_choice",
                    "detail": f"Relic tier {tier} is unlocked but no choice is recorded.",
                }
            )

    blessing_vector = state.get("blessing_path_vector", {})
    for key in ["t1", "t2", "t3", "t4", "t5", "t6"]:
        threshold = int(rules["blessings"]["steps"][key]["tasks"])
        if blessing_count >= threshold and blessing_vector.get(key) not in (1, 2, 3):
            warnings.append(
                {
                    "code": "unrecorded_blessing_choice",
                    "detail": f"Blessing {key} is unlocked but no path choice is recorded.",
                }
            )

    if missing_catalog_ids:
        errors.append(
            {
                "code": "unmapped_completed_tasks",
                "detail": f"Completed task IDs missing from catalog: {missing_catalog_ids}",
            }
        )

    return {
        "status": "error" if errors else ("warning" if warnings else "healthy"),
        "errors": errors,
        "warnings": warnings,
        "expected_elective_slots": expected_elective_slots,
        "recorded_elective_regions": selected_elective,
    }


def assistant_context(a, recommendations):
    account = a["account"]
    progression = a["progression"]
    lines = [
        f"# Equilibrium assistant state — {account['player']}",
        "",
        f"Updated: **{account['timestamp_utc']}**",
        "",
        "## Tracker discipline",
        "",
        "- `assistant-state.json` is the canonical assistant briefing.",
        "- `recommendations.json` is the canonical precomputed routing/sprint file.",
        "- `task-catalog.json` is the master 1,152-task database.",
        "- `player-state.json` contains only manual facts and choices.",
        "- `live-wikisync.json` is authoritative for completed task IDs and skill levels.",
        "- HiScores is optional and can never block task/skill refreshes.",
        "- Milestones come only from `league-rules.json`; never copy generated totals into manual state.",
        "- Recommendation grades: **A = explicit metadata**, **B = conservative inference**, **U = unknown**.",
        "",
        "## Current snapshot",
        "",
        f"- **{account['league_points']:,} LP** · **{account['completed_tasks']} tasks** · total level **{account['total_level']:,}**",
        f"- **{account['blessing_tasks_completed']} blessing tasks** · relic **T{progression['relic_tier']}**",
        f"- Regions: **{', '.join(a['regions']['unlocked'])}**",
    ]
    if progression.get("next_region"):
        lines.append(
            f"- Next region: **{progression['next_region']['remaining_tasks']} tasks** "
            f"to {progression['next_region']['tasks']}"
        )
    if progression.get("next_relic"):
        lines.append(
            f"- Next relic: **{progression['next_relic']['remaining_points']:,} LP** "
            f"to T{progression['next_relic']['tier']}"
        )
    if progression.get("next_blessing"):
        lines.append(
            f"- Next blessing step: **{progression['next_blessing']['remaining_tasks']}** "
            f"to {progression['next_blessing']['step']}"
        )

    lines += [
        "",
        "## Active relics",
        "",
        "Choice vector: `"
        + " ".join("-" if x is None else str(x) for x in a["relics"]["choice_vector"])
        + "`",
        "",
    ]
    for relic in a["relics"]["resolved"]:
        if not relic["unlocked"]:
            continue
        lines.append(f"### T{relic['tier']} — {relic['name'] or 'choice not recorded'}")
        lines += ["- " + effect for effect in relic["effects"]]
        passive = next(
            (p for p in a["relics"]["passive_by_tier"] if p["tier"] == relic["tier"]),
            None,
        )
        if passive:
            lines.append("Passive tier effects:")
            lines += ["- " + effect for effect in passive["effects"]]
        lines.append("")

    lines += [
        "## Active blessings",
        "",
        "Path encoding: `1=Order, 2=Balance, 3=Chaos`",
        "",
    ]
    for blessing in a["blessings"]["resolved"]:
        if not blessing["unlocked"]:
            continue
        lines.append(
            f"### {blessing['step']} — {blessing['name'] or 'choice not recorded'}"
            + (" (derived)" if blessing["derived"] else "")
        )
        lines += ["- " + effect for effect in blessing["effects"]]
        passive = next(
            (
                p
                for p in a["blessings"]["passive_by_step"]
                if p["step"] == blessing["step"]
            ),
            None,
        )
        if passive:
            lines.append("Passive step effects:")
            lines += ["- " + effect for effect in passive["effects"]]
        lines.append("")

    for dynamic in a["blessings"]["dynamic_effects"]:
        lines += [
            "### Dynamic blessing effect",
            "",
            f"- **{dynamic['source']}** currently has "
            f"**{dynamic['unique_paths_currently_chosen']} stacks**: "
            f"`{dynamic['current_bonus']}`",
            "",
        ]

    changes = a["changes"]
    lines += [
        "## Changes",
        "",
        f"- Tasks: **{changes['task_delta']:+d}** · LP: **{changes['league_points_delta']:+d}**",
    ]
    if changes["new_tasks"]:
        lines += [
            f"- [{task['id']}] {task['name']} — {task['tier']}, "
            f"{task['region']}, {task['points']} LP"
            for task in changes["new_tasks"]
        ]
    if changes["level_ups"]:
        lines.append(
            "- Level-ups: "
            + "; ".join(
                f"{x['skill']} {x['from']}→{x['to']}" for x in changes["level_ups"]
            )
        )

    sprint = recommendations["goal_sprint"]
    lines += [
        "",
        "## Current task sprint",
        "",
        f"- Need: **{sprint['tasks_needed']} tasks**",
        f"- Precomputed sprint: **{sprint['selected_count']} tasks** "
        f"({sprint['verified_count']} Grade A, {sprint['inferred_count']} Grade B)",
        f"- Action-time estimate excluding travel: "
        f"**{sprint['estimated_action_seconds_excluding_travel']} sec**",
    ]
    if sprint["prep_list"]:
        lines.append("- Prep: " + ", ".join(sprint["prep_list"]))
    for task in sprint["tasks"][:30]:
        lines.append(
            f"- [{task['id']}] **{task['name']}** — Grade "
            f"{task['recommendation_grade']} · ~{task['estimated_seconds']}s · "
            f"{task.get('cluster') or 'unclustered'}"
        )

    coverage = recommendations["coverage"]
    lines += [
        "",
        "## Recommendation coverage",
        "",
        f"- Timed Grade-A tasks: **{coverage['timed_verified_tasks']}**",
        f"- Timed Grade-B inferred candidates: **{coverage['timed_inferred_candidates']}**",
        f"- Metadata sources: `{coverage['metadata_source_counts']}`",
        "",
        "## Data health",
        "",
        f"- Overall: **{a['health']['overall']['status']}**",
        f"- WikiSync: **{a['health']['wikisync']['status']}** · "
        f"{a['health']['wikisync']['timestamp']}",
        f"- Task catalog: **{a['health']['task_catalog']['status']}** · "
        f"{a['health']['task_catalog']['task_count']} tasks",
        f"- HiScores: **{a['health']['hiscores']['status']}** (optional)",
    ]
    for warning in a["health"]["overall"]["warnings"]:
        lines.append(f"- WARNING `{warning['code']}`: {warning['detail']}")
    for error in a["health"]["overall"]["errors"]:
        lines.append(f"- ERROR `{error['code']}`: {error['detail']}")
    lines += [
        "",
        "> Always apply the active League effects above before normal RS3 mechanics.",
    ]
    return "\n".join(lines) + "\n"


def human_report(a, recommendations):
    account = a["account"]
    progression = a["progression"]
    sprint = recommendations["goal_sprint"]
    lines = [
        "# RS3 Equilibrium Tracker",
        "",
        f"Updated: **{account['timestamp_utc']}**",
        "",
        "## Current",
        "",
        f"- **{account['completed_tasks']} tasks**",
        f"- **{account['league_points']:,} LP**",
        f"- **Total level {account['total_level']:,}**",
        f"- **Relic T{progression['relic_tier']}**",
        f"- **{account['blessing_tasks_completed']} blessing tasks**",
        f"- Regions: {', '.join(a['regions']['unlocked'])}",
    ]
    if progression.get("next_region"):
        lines.append(
            f"- **{progression['next_region']['remaining_tasks']} tasks** to the next region slot"
        )
    if progression.get("next_relic"):
        lines.append(
            f"- **{progression['next_relic']['remaining_points']:,} LP** to T{progression['next_relic']['tier']}"
        )
    if progression.get("next_blessing"):
        lines.append(
            f"- **{progression['next_blessing']['remaining_tasks']} blessing tasks** "
            f"to {progression['next_blessing']['step']}"
        )

    lines += [
        "",
        "## Suggested sprint",
        "",
        f"Tracker selected **{sprint['selected_count']}** of the "
        f"**{sprint['tasks_needed']}** tasks currently needed.",
    ]
    if sprint["prep_list"]:
        lines.append("Prep once: " + ", ".join(sprint["prep_list"]))
    lines.append("")
    for task in sprint["tasks"]:
        lines.append(
            f"- [{task['id']}] {task['name']} — Grade {task['recommendation_grade']}, "
            f"~{task['estimated_seconds']}s, {task.get('cluster') or 'unclustered'}, "
            f"{task['points']} LP"
        )

    lines += ["", "## Best clusters", ""]
    for bundle in recommendations["cluster_bundles"][:12]:
        lines.append(
            f"- **{bundle['cluster']}** — {bundle['task_count']} candidates "
            f"({bundle['verified_count']} Grade A), {bundle['points']} LP"
        )

    lines += ["", "## Nearly unlocked", ""]
    if recommendations["nearly_unblocked"]:
        for task in recommendations["nearly_unblocked"][:15]:
            unlock = task["unlock"]
            lines.append(
                f"- [{task['id']}] {task['name']} — "
                f"{unlock['skill']} {unlock['current']}→{unlock['required']}"
            )
    else:
        lines.append("- None currently identified within 5 skill levels.")

    lines += ["", "## Health", ""]
    overall = a["health"]["overall"]
    lines.append(f"- **{overall['status']}**")
    for warning in overall["warnings"]:
        lines.append(f"- Warning: {warning['detail']}")
    for error in overall["errors"]:
        lines.append(f"- Error: {error['detail']}")

    lines += [
        "",
        "Grade A = explicit task metadata. Grade B = conservative automatic inference; verify before relying on it.",
    ]
    return "\n".join(lines) + "\n"


def main():
    now_dt = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    now = now_dt.isoformat()

    rules = load(ROOT / "league-rules.json", {})
    state = load(ROOT / "player-state.json", {})
    overrides = load(ROOT / "task-overrides.json", {}).get("tasks", {})
    wikisync = load(ROOT / "live-wikisync.json", {})

    if not isinstance(wikisync.get("league_tasks"), list) or not isinstance(
        wikisync.get("levels"), dict
    ):
        raise RuntimeError("WikiSync missing league_tasks or levels")

    tasks, catalog_status, catalog_time, catalog_change = catalog(now)
    by_id = {task["id"]: task for task in tasks}
    ids = sorted(set(int(x) for x in wikisync["league_tasks"]))
    done = set(ids)
    levels = {k: int(v) for k, v in wikisync["levels"].items()}
    completed = [by_id[x] for x in ids if x in by_id]
    missing = [x for x in ids if x not in by_id]
    lp = sum(task["points"] for task in completed)
    blessing_count = sum(1 for task in completed if task["blessing_task"])
    total_level = sum(levels.values())

    region_state = state.get("regions", {})
    unlocked = []
    for key in ("starting", "automatic", "elective"):
        for region in region_state.get(key, []) or []:
            if region not in unlocked:
                unlocked.append(region)
    regions = set(unlocked) | {"Global"}

    exclusions = {
        int(k): v for k, v in state.get("task_exclusions", {}).items()
    }
    flags = state.get("manual_flags", {})

    unfinished = [
        evaluate(
            task,
            overrides.get(str(task["id"])),
            levels,
            regions,
            exclusions,
            flags,
        )
        for task in tasks
        if task["id"] not in done
    ]
    counts = collections.Counter(task["status"] for task in unfinished)

    old = load(ROOT / "live-summary.json", {})
    old_ids = set(int(x) for x in old.get("completed_task_ids", []) or [])
    new_ids = sorted(done - old_ids)
    old_levels = {k: int(v) for k, v in old.get("levels", {}).items()}
    level_ups = [
        {
            "skill": skill,
            "from": old_levels.get(skill, level),
            "to": level,
        }
        for skill, level in levels.items()
        if level > old_levels.get(skill, level)
    ]
    changes = {
        "task_delta": len(ids) - len(old_ids) if old_ids else 0,
        "league_points_delta": lp - int(old.get("league_points", lp) or lp),
        "new_task_ids": new_ids,
        "new_tasks": [by_id[x] for x in new_ids if x in by_id],
        "level_ups": level_ups,
    }

    current_relic_tier = relic_tier(rules, lp)
    relics, relic_passives = resolve_relics(rules, state, current_relic_tier)
    current_blessing_step, next_blessing = blessing_progress(rules, blessing_count)
    blessings, blessing_passives, gods, dynamic = resolve_blessings(
        rules, state, blessing_count
    )

    progression = {
        "relic_tier": current_relic_tier,
        "next_relic": next_relic(rules, lp),
        "next_region": next_region(rules, len(ids)),
        "current_blessing_step": current_blessing_step,
        "next_blessing": next_blessing,
    }
    recommendations = recommendation_bundle(unfinished, progression, state)

    hiscores_path = ROOT / "live-hiscores.html"
    hiscores_present = hiscores_path.exists() and hiscores_path.stat().st_size > 0
    state_validation = validate_state(
        rules,
        state,
        len(ids),
        current_relic_tier,
        blessing_count,
        missing,
    )
    health = {
        "generated_at_utc": wikisync.get("timestamp") or now,
        "overall": state_validation,
        "wikisync": {
            "status": "fresh" if wikisync.get("timestamp") else "present_no_timestamp",
            "timestamp": wikisync.get("timestamp"),
            "age_seconds_at_generation": age_seconds(wikisync.get("timestamp"), now_dt),
            "authoritative_for": ["completed_task_ids", "skill_levels"],
        },
        "task_catalog": {
            "status": catalog_status,
            "fetched_at_utc": catalog_time,
            "age_seconds_at_generation": age_seconds(catalog_time, now_dt),
            "task_count": len(tasks),
            "mapped_completed_tasks": len(completed),
            "unmapped_completed_task_ids": missing,
            "latest_change_check": catalog_change,
        },
        "hiscores": {
            "status": "fetched_optional" if hiscores_present else "unavailable_optional",
            "required": False,
            "note": "HiScores parsing is not a dependency.",
        },
        "recommendation_coverage": recommendations["coverage"],
    }

    assistant_state = {
        "schema_version": 2,
        "account": {
            "timestamp_utc": wikisync.get("timestamp") or now,
            "player": state.get("player") or wikisync.get("username"),
            "league": state.get("league"),
            "league_points": lp,
            "league_points_source": "sum of mapped completed task points",
            "completed_tasks": len(ids),
            "completed_task_ids": ids,
            "total_level": total_level,
            "levels": levels,
            "blessing_tasks_completed": blessing_count,
        },
        "progression": progression,
        "regions": {"unlocked": unlocked, **region_state},
        "relics": {
            "choice_vector": state.get("relic_choice_vector", []),
            "resolved": relics,
            "passive_by_tier": relic_passives,
        },
        "blessings": {
            "path_encoding": rules["blessings"]["path_encoding"],
            "path_vector": state.get("blessing_path_vector", {}),
            "derived_god_choices": gods,
            "resets_remaining": state.get("blessing_resets_remaining"),
            "resolved": blessings,
            "passive_by_step": blessing_passives,
            "dynamic_effects": dynamic,
        },
        "manual": {
            "goal": state.get("goal"),
            "key_items": state.get("key_items", []),
            "route_preferences": state.get("route_preferences", {}),
            "task_exclusions": state.get("task_exclusions", {}),
            "manual_flags": flags,
        },
        "tasks": {
            "master_task_count": len(tasks),
            "unfinished_count": len(unfinished),
            "status_counts": dict(sorted(counts.items())),
            "verified_ready_count": counts.get("verified_ready", 0),
            "inferred_candidate_count": counts.get("inferred_candidate", 0),
            "manual_check_count": counts.get("manual_check", 0),
            "requirements_unknown_count": counts.get(
                "accessible_requirements_unknown", 0
            ),
            "recommendations_file": "recommendations.json",
        },
        "changes": changes,
        "health": health,
    }

    summary = {
        "timestamp_utc": assistant_state["account"]["timestamp_utc"],
        "player": assistant_state["account"]["player"],
        "source": "WikiSync + master Equilibrium task catalog; HiScores optional",
        "league_points": lp,
        "league_points_source": "mapped completed-task point sum",
        "completed_tasks": len(ids),
        "completed_task_ids": ids,
        "total_level": total_level,
        "levels": levels,
        "blessing_tasks_completed": blessing_count,
        "relic_tier": current_relic_tier,
        "next_relic": progression["next_relic"],
        "next_region": progression["next_region"],
        "next_blessing": progression["next_blessing"],
        "new_task_ids_since_previous_live_sync": new_ids,
        "new_tasks_since_previous_live_sync": changes["new_tasks"],
        "task_delta_since_previous_live_sync": changes["task_delta"],
        "level_ups_since_previous_live_sync": level_ups,
        "catalog_task_count": len(tasks),
        "mapped_completed_tasks": len(completed),
        "unmapped_completed_task_ids": missing,
        "confirmed_unlocked_regions": unlocked,
        "relic_choice_vector": state.get("relic_choice_vector", []),
        "blessing_path_vector": state.get("blessing_path_vector", {}),
        "excluded_recommendation_task_ids": sorted(exclusions),
        "tracker_health": state_validation["status"],
    }

    unfinished_doc = {
        "schema_version": 3,
        "timestamp_utc": assistant_state["account"]["timestamp_utc"],
        "master_task_count": len(tasks),
        "completed_task_count": len(ids),
        "unfinished_task_count": len(unfinished),
        "unlocked_regions": unlocked,
        "status_counts": dict(sorted(counts.items())),
        "recommendations_file": "recommendations.json",
        "unfinished_tasks": unfinished,
    }

    history = load(ROOT / "live-history.json", [])
    history = history if isinstance(history, list) else []
    snapshot = {
        "timestamp_utc": assistant_state["account"]["timestamp_utc"],
        "completed_tasks": len(ids),
        "league_points": lp,
        "total_level": total_level,
        "blessing_tasks_completed": blessing_count,
        "levels": levels,
        "regions": unlocked,
        "relic_tier": current_relic_tier,
    }
    if not history or any(
        history[-1].get(key) != snapshot[key]
        for key in (
            "completed_tasks",
            "league_points",
            "total_level",
            "blessing_tasks_completed",
            "regions",
            "relic_tier",
        )
    ):
        history = (history + [snapshot])[-200:]

    dump(ROOT / "assistant-state.json", assistant_state)
    dump(ROOT / "live-summary.json", summary)
    dump(ROOT / "live-unfinished.json", unfinished_doc)
    dump(ROOT / "recommendations.json", recommendations)
    dump(ROOT / "changes.json", changes)
    dump(ROOT / "health.json", health)
    dump(ROOT / "catalog-changes.json", catalog_change)
    dump(ROOT / "live-history.json", history)
    (ROOT / "assistant-context.md").write_text(
        assistant_context(assistant_state, recommendations),
        encoding="utf-8",
    )
    (ROOT / "report.md").write_text(
        human_report(assistant_state, recommendations),
        encoding="utf-8",
    )

    print(
        f"Equilibrium tracker: {len(ids)} tasks | {lp} LP | total {total_level} | "
        f"{blessing_count} blessings | T{current_relic_tier} | "
        f"catalog {catalog_status}:{len(tasks)} | "
        f"Grade-A timed {recommendations['coverage']['timed_verified_tasks']} | "
        f"Grade-B timed {recommendations['coverage']['timed_inferred_candidates']}"
    )


if __name__ == "__main__":
    main()
