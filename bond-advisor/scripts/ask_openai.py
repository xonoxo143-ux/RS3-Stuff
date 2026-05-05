from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv

from _common import OUTPUT_DIR, load_json, now_iso, write_json

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def compact_for_ai(context: Dict[str, Any], scored: Dict[str, Any]) -> Dict[str, Any]:
    character = context.get("character", {})
    market = context.get("market", {})
    return {
        "built_at": context.get("built_at"),
        "character": {
            "rsn": character.get("rsn"),
            "coins": (character.get("coins") or {}).get("value"),
            "preferences": character.get("preferences", {}),
            "manual_unlocks": character.get("manual_unlocks", {}),
            "gear_summary": character.get("gear_summary", {}),
            "bank_notes": character.get("bank_notes", {}),
            "hiscores_summary": {
                "status": (((character.get("hiscores") or {}).get("source_status") or {}).get("status")),
                "skills": ((character.get("hiscores") or {}).get("skills") or {}).get("value", {}),
            },
            "runemetrics_profile_summary": ((character.get("runemetrics_profile") or {}).get("summary") or {}).get("value", {}),
            "quest_summary": ((character.get("runemetrics_quests") or {}).get("summary") or {}).get("value", {}),
        },
        "market": {
            "bond_price": market.get("bond_price", {}),
            "daily_target_gp": market.get("daily_target_gp", {}),
            "safe_daily_target_gp": market.get("safe_daily_target_gp", {}),
            "itemdb_bond": (((market.get("itemdb") or {}).get("items") or {}).get("29492") or {}),
            "wiki_price_status": (market.get("wiki_prices") or {}).get("latest_status", {}),
        },
        "ranked_methods": scored.get("all_methods_ranked", []),
        "uncertainties": context.get("uncertainties", []),
        "scoring_notes": scored.get("notes", []),
    }


def fallback_plan(context: Dict[str, Any], scored: Dict[str, Any], reason: str) -> Dict[str, Any]:
    market = context.get("market", {})
    strong = scored.get("strong_methods", [])
    usable = scored.get("usable_methods", [])
    blocked = scored.get("blocked_methods", [])
    best = (strong + usable)[:5]
    return {
        "schema_version": "0.5",
        "generated_at": now_iso(),
        "source": "local_fallback",
        "model": None,
        "daily_target_gp": (market.get("safe_daily_target_gp") or {}).get("value"),
        "headline": "Local fallback plan generated because OpenAI was unavailable.",
        "recommended_plan": [
            {
                "method_id": method.get("id"),
                "method_name": method.get("name"),
                "priority": index + 1,
                "expected_gp": None,
                "time_minutes": None,
                "confidence": "low" if method.get("tier") == "weak" else "medium",
                "reason": "; ".join(method.get("reasons", [])[:3]),
                "next_action": "Review this method manually before relying on it. Method catalog is still early.",
            }
            for index, method in enumerate(best)
        ],
        "avoid_today": [
            {
                "method_id": method.get("id"),
                "method_name": method.get("name"),
                "reason": "; ".join(method.get("blockers", [])[:3]) or "Low score.",
            }
            for method in blocked[:5]
        ],
        "confidence_notes": [
            reason,
            "No OpenAI reasoning was used for this file.",
            "Use the scored methods file for raw ranking details.",
        ],
        "missing_info_needed": context.get("uncertainties", []),
    }


def render_markdown(plan: Dict[str, Any]) -> str:
    lines = []
    lines.append("# RS3 Bond Sustainer Daily Plan")
    lines.append("")
    lines.append(f"Generated: {plan.get('generated_at')}")
    lines.append(f"Source: {plan.get('source')}")
    lines.append("")
    lines.append(f"## Headline\n\n{plan.get('headline', 'No headline provided.')}")
    lines.append("")
    lines.append(f"## Daily target\n\n{plan.get('daily_target_gp') or 'Unknown'} GP")
    lines.append("")
    lines.append("## Recommended plan")
    lines.append("")
    recommendations = plan.get("recommended_plan") or []
    if recommendations:
        for item in recommendations:
            lines.append(f"### {item.get('priority', '-')}. {item.get('method_name') or item.get('method_id')}")
            lines.append("")
            lines.append(f"- Confidence: {item.get('confidence')}")
            lines.append(f"- Time: {item.get('time_minutes') or 'Not estimated'} minutes")
            lines.append(f"- Expected GP: {item.get('expected_gp') or 'Not estimated'}")
            lines.append(f"- Why: {item.get('reason')}")
            lines.append(f"- Next action: {item.get('next_action')}")
            lines.append("")
    else:
        lines.append("No recommended methods yet. Expand the method catalog and profile data.")
        lines.append("")

    lines.append("## Avoid today")
    lines.append("")
    avoids = plan.get("avoid_today") or []
    if avoids:
        for item in avoids:
            lines.append(f"- {item.get('method_name') or item.get('method_id')}: {item.get('reason')}")
    else:
        lines.append("No avoid list generated.")
    lines.append("")

    lines.append("## Missing info / confidence notes")
    lines.append("")
    for note in (plan.get("missing_info_needed") or []) + (plan.get("confidence_notes") or []):
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def call_openai(context: Dict[str, Any], scored: Dict[str, Any], model: str) -> Dict[str, Any]:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return fallback_plan(context, scored, "OPENAI_API_KEY is not set.")

    payload = compact_for_ai(context, scored)
    instructions = (
        "You are an RS3 bond-sustaining planning assistant. "
        "Use only the provided data. Do not invent live prices, unlocks, or guaranteed gp/hr. "
        "Treat RuneScape gameplay automation as out of scope. Produce legal manual advice only. "
        "Be conservative, mobile-aware, and direct. If data is missing, say so."
    )
    user_text = (
        "Create a realistic RS3 bond-sustain daily plan from this JSON. "
        "Return JSON only with keys: schema_version, generated_at, source, model, daily_target_gp, headline, "
        "recommended_plan, avoid_today, confidence_notes, missing_info_needed.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )

    body = {
        "model": model,
        "input": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_text},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "rs3_bond_daily_plan",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "schema_version",
                        "generated_at",
                        "source",
                        "model",
                        "daily_target_gp",
                        "headline",
                        "recommended_plan",
                        "avoid_today",
                        "confidence_notes",
                        "missing_info_needed",
                    ],
                    "properties": {
                        "schema_version": {"type": "string"},
                        "generated_at": {"type": "string"},
                        "source": {"type": "string"},
                        "model": {"type": "string"},
                        "daily_target_gp": {"type": ["integer", "null"]},
                        "headline": {"type": "string"},
                        "recommended_plan": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["method_id", "method_name", "priority", "expected_gp", "time_minutes", "confidence", "reason", "next_action"],
                                "properties": {
                                    "method_id": {"type": ["string", "null"]},
                                    "method_name": {"type": ["string", "null"]},
                                    "priority": {"type": "integer"},
                                    "expected_gp": {"type": ["integer", "null"]},
                                    "time_minutes": {"type": ["integer", "null"]},
                                    "confidence": {"type": "string"},
                                    "reason": {"type": "string"},
                                    "next_action": {"type": "string"},
                                },
                            },
                        },
                        "avoid_today": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["method_id", "method_name", "reason"],
                                "properties": {
                                    "method_id": {"type": ["string", "null"]},
                                    "method_name": {"type": ["string", "null"]},
                                    "reason": {"type": "string"},
                                },
                            },
                        },
                        "confidence_notes": {"type": "array", "items": {"type": "string"}},
                        "missing_info_needed": {"type": "array", "items": {"type": "string"}},
                    },
                },
            }
        },
    }

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    if not response.ok:
        return fallback_plan(context, scored, f"OpenAI request failed: HTTP {response.status_code}: {response.text[:500]}")

    data = response.json()
    output_text = data.get("output_text")
    if not output_text:
        # Fallback parser for Responses API output array.
        parts = []
        for item in data.get("output", []) or []:
            for content in item.get("content", []) or []:
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    parts.append(content["text"])
        output_text = "".join(parts)

    try:
        plan = json.loads(output_text)
    except Exception as exc:
        return fallback_plan(context, scored, f"OpenAI returned non-JSON or unparseable output: {exc}")

    plan["generated_at"] = plan.get("generated_at") or now_iso()
    plan["source"] = "openai"
    plan["model"] = model
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate daily plan with OpenAI or local fallback.")
    parser.add_argument("--context", default=str(OUTPUT_DIR / "bond_advisor_context.json"))
    parser.add_argument("--scored", default=str(OUTPUT_DIR / "scored_methods.json"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    context = load_json(Path(args.context), default={}) or {}
    scored = load_json(Path(args.scored), default={}) or {}
    if not context:
        raise SystemExit("Missing context. Run scripts/build_context.py first.")
    if not scored:
        raise SystemExit("Missing scored methods. Run scripts/score_methods.py first.")

    plan = call_openai(context, scored, args.model)
    write_json(OUTPUT_DIR / "daily_plan.json", plan)
    (OUTPUT_DIR / "daily_plan.md").write_text(render_markdown(plan), encoding="utf-8")
    print(f"Wrote {OUTPUT_DIR / 'daily_plan.json'}")
    print(f"Wrote {OUTPUT_DIR / 'daily_plan.md'}")


if __name__ == "__main__":
    main()
