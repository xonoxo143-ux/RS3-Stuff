from __future__ import annotations

import argparse
from typing import Any, Dict, List, Tuple

from _common import OUTPUT_DIR, load_json, now_iso, write_json


def get_skill_levels(context: Dict[str, Any]) -> Dict[str, int]:
    skills = (((context.get("character") or {}).get("hiscores") or {}).get("skills") or {}).get("value") or {}
    out: Dict[str, int] = {}
    for name, record in skills.items():
        if isinstance(record, dict):
            try:
                out[str(name).lower()] = int(record.get("level", 0))
            except (TypeError, ValueError):
                out[str(name).lower()] = 0
    return out


def get_completed_quest_titles(context: Dict[str, Any]) -> set[str]:
    quests = ((((context.get("character") or {}).get("runemetrics_quests") or {}).get("quests") or {}).get("value")) or []
    completed = set()
    for quest in quests:
        if not isinstance(quest, dict):
            continue
        status = str(quest.get("status", "")).lower()
        title = str(quest.get("title", "")).strip().lower()
        if title and status in {"completed", "complete"}:
            completed.add(title)
    return completed


def normalize_list(values: Any) -> set[str]:
    if not isinstance(values, list):
        return set()
    return {str(v).strip().lower() for v in values if str(v).strip()}


def get_unlocks(context: Dict[str, Any]) -> set[str]:
    manual_unlocks = ((context.get("character") or {}).get("manual_unlocks") or {})
    unlocked = set()
    if isinstance(manual_unlocks, dict):
        for key, value in manual_unlocks.items():
            if value is True:
                unlocked.add(str(key).lower())
            elif isinstance(value, list):
                for item in value:
                    unlocked.add(str(item).lower())
    return unlocked


def score_attention(method_attention: str, preferred_attention: str) -> Tuple[int, str]:
    method_attention = (method_attention or "medium").lower()
    preferred_attention = (preferred_attention or "medium").lower()
    order = {"low": 0, "medium": 1, "high": 2}
    if method_attention == preferred_attention:
        return 12, "matches preferred attention"
    if order.get(method_attention, 1) < order.get(preferred_attention, 1):
        return 8, "below preferred attention; likely tolerable"
    if order.get(method_attention, 1) == order.get(preferred_attention, 1) + 1:
        return -4, "slightly above preferred attention"
    return -12, "well above preferred attention"


def score_mobile(method_mobile: str, mobile_only: bool) -> Tuple[int, str]:
    method_mobile = (method_mobile or "medium").lower()
    if not mobile_only:
        return 0, "mobile-only filter not active"
    if method_mobile == "high":
        return 18, "mobile-friendly"
    if method_mobile == "medium":
        return 6, "moderately mobile-friendly"
    return -25, "poor mobile fit"


def score_market_risk(risk: str) -> Tuple[int, str]:
    risk = (risk or "medium").lower()
    if risk == "low":
        return 12, "low market risk"
    if risk == "medium":
        return 3, "medium market risk"
    return -12, "high market risk"


def evaluate_method(context: Dict[str, Any], method: Dict[str, Any]) -> Dict[str, Any]:
    skills = get_skill_levels(context)
    completed_quests = get_completed_quest_titles(context)
    unlocks = get_unlocks(context)
    preferences = ((context.get("character") or {}).get("preferences") or {})
    preferred_attention = preferences.get("preferred_attention", "medium")
    mobile_only = bool(preferences.get("mobile_only", True))
    methods_to_avoid = normalize_list(preferences.get("methods_to_avoid", []))
    methods_you_like = normalize_list(preferences.get("methods_you_like", []))
    coins = ((((context.get("character") or {}).get("coins") or {}).get("value"))) or 0

    missing_skills = []
    for skill, required_level in (method.get("required_skills") or {}).items():
        current = skills.get(str(skill).lower(), 0)
        try:
            required = int(required_level)
        except (TypeError, ValueError):
            required = 0
        if current < required:
            missing_skills.append({"skill": skill, "required": required, "current": current})

    missing_quests = []
    for quest in method.get("required_quests") or []:
        quest_key = str(quest).strip().lower()
        if quest_key and quest_key not in completed_quests:
            missing_quests.append(str(quest))

    missing_unlocks = []
    for unlock in method.get("required_unlocks") or []:
        unlock_key = str(unlock).strip().lower()
        if unlock_key and unlock_key not in unlocks:
            missing_unlocks.append(str(unlock))

    setup_cost_gp = int(method.get("setup_cost_gp") or 0)
    setup_cost_issue = setup_cost_gp > 0 and isinstance(coins, int) and coins > 0 and setup_cost_gp > coins

    method_id = str(method.get("id", "")).lower()
    method_name = str(method.get("name", "")).lower()
    avoided_by_user = method_id in methods_to_avoid or method_name in methods_to_avoid
    liked_by_user = method_id in methods_you_like or method_name in methods_you_like

    score = 40
    reasons: List[str] = []
    blockers: List[str] = []

    if missing_skills:
        score -= 40
        blockers.append("missing required skill levels")
    else:
        score += 15
        reasons.append("skill requirements met or not required")

    if missing_quests:
        score -= 25
        blockers.append("missing required quests or quest data unavailable")
    else:
        score += 8
        reasons.append("quest requirements met or not required")

    if missing_unlocks:
        score -= 25
        blockers.append("missing required unlocks")
    else:
        score += 8
        reasons.append("unlock requirements met or not required")

    if setup_cost_issue:
        score -= 20
        blockers.append("setup cost appears above available coins")

    mobile_score, mobile_reason = score_mobile(str(method.get("mobile_friendliness", "medium")), mobile_only)
    score += mobile_score
    reasons.append(mobile_reason)

    attention_score, attention_reason = score_attention(str(method.get("attention", "medium")), str(preferred_attention))
    score += attention_score
    reasons.append(attention_reason)

    market_score, market_reason = score_market_risk(str(method.get("market_risk", "medium")))
    score += market_score
    reasons.append(market_reason)

    if avoided_by_user:
        score -= 60
        blockers.append("user marked this method to avoid")
    if liked_by_user:
        score += 15
        reasons.append("user marked this method as liked")

    eligible = not missing_skills and not missing_quests and not missing_unlocks and not avoided_by_user and not setup_cost_issue
    if eligible and score >= 70:
        tier = "strong"
    elif eligible and score >= 45:
        tier = "usable"
    elif eligible:
        tier = "weak"
    else:
        tier = "blocked"

    return {
        "id": method.get("id"),
        "name": method.get("name"),
        "category": method.get("category"),
        "eligible": eligible,
        "tier": tier,
        "score": score,
        "missing_skills": missing_skills,
        "missing_quests": missing_quests,
        "missing_unlocks": missing_unlocks,
        "blockers": blockers,
        "reasons": reasons,
        "attention": method.get("attention"),
        "mobile_friendliness": method.get("mobile_friendliness"),
        "market_risk": method.get("market_risk"),
        "setup_cost_gp": setup_cost_gp,
        "notes": method.get("notes", ""),
    }


def score_methods(context: Dict[str, Any]) -> Dict[str, Any]:
    methods = ((context.get("methods") or {}).get("methods")) or []
    scored = [evaluate_method(context, method) for method in methods if isinstance(method, dict)]
    scored.sort(key=lambda item: item.get("score", 0), reverse=True)

    return {
        "schema_version": "0.4",
        "generated_at": now_iso(),
        "method_count": len(scored),
        "strong_methods": [m for m in scored if m.get("tier") == "strong"],
        "usable_methods": [m for m in scored if m.get("tier") == "usable"],
        "weak_methods": [m for m in scored if m.get("tier") == "weak"],
        "blocked_methods": [m for m in scored if m.get("tier") == "blocked"],
        "all_methods_ranked": scored,
        "notes": [
            "This is a conservative pre-AI score. It checks fit and blockers, not final gp/hr.",
            "Method catalog values are placeholders until expanded and validated.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score methods from bond_advisor_context.json.")
    parser.add_argument("--context", default=str(OUTPUT_DIR / "bond_advisor_context.json"), help="Context JSON path.")
    args = parser.parse_args()

    context = load_json(Path(args.context), default={}) or {}
    if not context:
        raise SystemExit("No context loaded. Run scripts/build_context.py first.")

    result = score_methods(context)
    write_json(OUTPUT_DIR / "scored_methods.json", result)
    print(f"Wrote {OUTPUT_DIR / 'scored_methods.json'}")


if __name__ == "__main__":
    main()
