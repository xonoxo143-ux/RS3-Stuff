#!/usr/bin/env python3
"""Conservative task metadata inference for the Equilibrium tracker.

This module intentionally prefers UNKNOWN over a confident-looking bad guess.
Manual task-overrides.json metadata always wins over inferred metadata.
"""
import re

SKILLS = [
    "Attack", "Defence", "Strength", "Constitution", "Ranged", "Prayer", "Magic",
    "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting",
    "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming",
    "Runecrafting", "Hunter", "Construction", "Summoning", "Dungeoneering",
    "Divination", "Invention", "Archaeology", "Necromancy",
]

CLUSTERS = [
    (r"pyramid plunder|sophanem", "sophanem_pyramid_plunder"),
    (r"fort forinthry|fort workshop", "fort_forinthry"),
    (r"al kharid", "al_kharid"),
    (r"het'?s oasis", "hets_oasis"),
    (r"brimhaven dungeon", "brimhaven_dungeon"),
    (r"brimhaven", "brimhaven"),
    (r"shilo village", "shilo_village"),
    (r"karamja", "karamja"),
    (r"lumbridge", "lumbridge"),
    (r"draynor", "draynor"),
    (r"varrock", "varrock"),
    (r"menaphos", "menaphos"),
    (r"havenhythe", "havenhythe"),
    (r"city of um|\bum\b", "city_of_um"),
]

# Only actions that are usually short once the player is at the right place / has prep.
# These are candidates, never treated as verified unless task-overrides.json confirms them.
ACTION_RULES = [
    (r"^drink\b", 10, "consume"),
    (r"^eat\b", 10, "consume"),
    (r"^(equip|wear)\b", 20, "equip"),
    (r"^perform (a|an) .*special attack", 10, "combat_action"),
    (r"^(talk|speak)\b", 30, "npc"),
    (r"^search\b", 30, "search"),
    (r"^enter\b", 30, "travel"),
    (r"^use\b", 30, "use"),
    (r"^claim\b", 30, "claim"),
    (r"^(buy|sell)\b", 45, "shop"),
    (r"^pick a\b", 30, "gather"),
    (r"^pick \d+\b", 75, "gather"),
    (r"^churn\b", 45, "cooking"),
    (r"^(bake|cook)\b", 60, "cooking"),
    (r"^(fletch|craft|make|smith)\b", 60, "production"),
    (r"^mine a\b", 45, "mining"),
    (r"^catch (a|an|shrimp)\b", 45, "fishing_or_hunter"),
    (r"^scatter \d+\b", 60, "prayer"),
]

# Task wording that is too likely to hide meaningful progression/grind requirements.
SLOW_OR_COMPLEX = re.compile(
    r"\b(complete|fully complete|quest|achievement set|clue|laps?|slayer tasks?|kill \d+|defeat \d+|"
    r"obtain|earn \d+|gain \d+|reach total level|prestige|collection log|boss log|"
    r"reputation|deliver \d+|restore \d+|excavate \d+)\b",
    re.I,
)


def _skill_requirements(text):
    out = {}
    low = text.lower()
    for skill in SKILLS:
        s = re.escape(skill.lower())
        patterns = [
            rf"(?:reach|attain|get|have)\s+(?:level\s+)?(\d{{1,3}})\s+(?:in\s+)?{s}\b",
            rf"(?:level|at least)\s+(\d{{1,3}})\s+(?:in\s+)?{s}\b",
            rf"\b{s}\s+(?:level\s+)?(\d{{1,3}})\b",
        ]
        vals = []
        for pattern in patterns:
            vals.extend(int(x) for x in re.findall(pattern, low, re.I))
        if vals:
            out[skill] = max(vals)
    return out


def _cluster(text):
    for pattern, name in CLUSTERS:
        if re.search(pattern, text, re.I):
            return name
    return None


def _action(text):
    if SLOW_OR_COMPLEX.search(text):
        return None, None
    for pattern, seconds, tag in ACTION_RULES:
        if re.search(pattern, text, re.I):
            # Large explicit quantities are not one-click tasks. Keep the metadata but
            # do not generate a fast-time estimate from the verb alone.
            nums = [int(x) for x in re.findall(r"\b(\d{2,})\b", text)]
            if nums and max(nums) > 25 and tag not in {"equip", "consume"}:
                return None, tag
            return seconds, tag
    return None, None


def infer_task(task):
    text = f"{task.get('name', '')} {task.get('description', '')}".strip()
    seconds, action_tag = _action(text)
    skills = _skill_requirements(text)
    cluster = _cluster(text)
    tags = ["inferred"]
    if action_tag:
        tags.append(action_tag)
    for skill in SKILLS:
        if skill.lower() in text.lower():
            tags.append(skill.lower().replace(" ", "_"))
    tags = list(dict.fromkeys(tags))

    # A candidate only gets a fast estimate when the wording is conservative enough.
    confidence = 0.72 if seconds is not None else (0.55 if skills or cluster else 0.0)
    return {
        "source": "text_inference" if confidence else "none",
        "confidence": confidence,
        "estimated_seconds": seconds,
        "cluster": cluster,
        "tags": tags if confidence else [],
        "skills": skills,
        "items": [],
        "manual_requirements": [],
    }


def merge_metadata(task, override):
    inferred = infer_task(task)
    if not override:
        return inferred
    merged = dict(inferred)
    merged.update({k: v for k, v in override.items() if k not in {"skills", "tags", "items", "manual_requirements"}})
    merged["skills"] = {**inferred.get("skills", {}), **(override.get("skills") or {})}
    merged["tags"] = list(dict.fromkeys((inferred.get("tags") or []) + (override.get("tags") or [])))
    merged["items"] = list(override.get("items") or inferred.get("items") or [])
    merged["manual_requirements"] = list(override.get("manual_requirements") or [])
    merged["source"] = "manual_override"
    merged["confidence"] = float(override.get("confidence", 1.0))
    return merged


def recommendation_metrics(task):
    seconds = task.get("estimated_seconds")
    points = int(task.get("points") or 0)
    confidence = float(task.get("confidence") or 0)
    if not seconds:
        return {"lp_per_minute": None, "task_count_efficiency": None, "recommendation_grade": "U"}
    lp_per_minute = round(points * 60 / max(seconds, 1), 2)
    # Lower is better. Uncertainty adds a large penalty so verified tasks sort first.
    uncertainty_penalty = round((1.0 - confidence) * 180)
    task_count_efficiency = int(seconds) + uncertainty_penalty
    if task.get("metadata_source") == "manual_override" and confidence >= 0.95:
        grade = "A"
    elif confidence >= 0.7:
        grade = "B"
    else:
        grade = "C"
    return {
        "lp_per_minute": lp_per_minute,
        "task_count_efficiency": task_count_efficiency,
        "recommendation_grade": grade,
    }
