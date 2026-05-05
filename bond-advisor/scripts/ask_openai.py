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
GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


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
        "schema_version": "0.6",
        "generated_at": now_iso(),
        "source": "local_fallback",
        "model": None,
        "daily_target_gp": (market.get("safe_daily_target_gp") or {}).get("value"),
        "headline": "Local fallback plan generated because the configured LLM provider was unavailable.",
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
            "No external LLM reasoning was used for this file.",
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
    lines.append(f"Model: {plan.get('model') or 'none'}")
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


def plan_prompt(context: Dict[str, Any], scored: Dict[str, Any]) -> tuple[str, str]:
    payload = compact_for_ai(context, scored)
    instructions = (
        "You are an RS3 bond-sustaining planning assistant. "
        "Use only the provided data. Do not invent live prices, unlocks, or guaranteed gp/hr. "
        "Treat RuneScape gameplay automation as out of scope. Produce legal manual advice only. "
        "Be conservative, mobile-aware, and direct. If data is missing, say so. "
        "Return valid JSON only."
    )
    user_text = (
        "Create a realistic RS3 bond-sustain daily plan from this JSON. "
        "Return JSON only with exactly these keys: schema_version, generated_at, source, model, daily_target_gp, headline, "
        "recommended_plan, avoid_today, confidence_notes, missing_info_needed.\n\n"
        "recommended_plan items must have: method_id, method_name, priority, expected_gp, time_minutes, confidence, reason, next_action.\n"
        "avoid_today items must have: method_id, method_name, reason.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    return instructions, user_text


def normalize_plan(plan: Dict[str, Any], source: str, model: str) -> Dict[str, Any]:
    return {
        "schema_version": str(plan.get("schema_version") or "0.6"),
        "generated_at": str(plan.get("generated_at") or now_iso()),
        "source": source,
        "model": model,
        "daily_target_gp": plan.get("daily_target_gp"),
        "headline": str(plan.get("headline") or "No headline provided."),
        "recommended_plan": plan.get("recommended_plan") if isinstance(plan.get("recommended_plan"), list) else [],
        "avoid_today": plan.get("avoid_today") if isinstance(plan.get("avoid_today"), list) else [],
        "confidence_notes": plan.get("confidence_notes") if isinstance(plan.get("confidence_notes"), list) else [],
        "missing_info_needed": plan.get("missing_info_needed") if isinstance(plan.get("missing_info_needed"), list) else [],
    }


def parse_json_plan(text: str) -> Dict[str, Any]:
    text = (text or "").strip()
    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()
    if text.startswith("```"):
        text = text.removeprefix("```").strip()
    if text.endswith("```"):
        text = text.removesuffix("```").strip()
    return json.loads(text)


def call_groq(context: Dict[str, Any], scored: Dict[str, Any], model: str) -> Dict[str, Any]:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return fallback_plan(context, scored, "GROQ_API_KEY is not set.")

    instructions, user_text = plan_prompt(context, scored)
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.2,
        "max_completion_tokens": 1800,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        GROQ_CHAT_COMPLETIONS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    if not response.ok:
        return fallback_plan(context, scored, f"Groq request failed: HTTP {response.status_code}: {response.text[:500]}")

    data = response.json()
    try:
        output_text = data["choices"][0]["message"]["content"]
        return normalize_plan(parse_json_plan(output_text), "groq", model)
    except Exception as exc:
        return fallback_plan(context, scored, f"Groq returned unparseable output: {exc}")


def call_openai(context: Dict[str, Any], scored: Dict[str, Any], model: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return fallback_plan(context, scored, "OPENAI_API_KEY is not set.")

    instructions, user_text = plan_prompt(context, scored)
    body = {
        "model": model,
        "input": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_text},
        ],
        "text": {"format": {"type": "json_object"}},
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
        parts = []
        for item in data.get("output", []) or []:
            for content in item.get("content", []) or []:
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    parts.append(content["text"])
        output_text = "".join(parts)

    try:
        return normalize_plan(parse_json_plan(output_text), "openai", model)
    except Exception as exc:
        return fallback_plan(context, scored, f"OpenAI returned non-JSON or unparseable output: {exc}")


def choose_provider(cli_provider: str) -> str:
    provider = (cli_provider or os.getenv("ADVISOR_LLM_PROVIDER", "auto")).strip().lower()
    if provider in {"groq", "openai", "none"}:
        return provider
    if os.getenv("GROQ_API_KEY", "").strip():
        return "groq"
    if os.getenv("OPENAI_API_KEY", "").strip():
        return "openai"
    return "none"


def generate_plan(context: Dict[str, Any], scored: Dict[str, Any], provider: str, openai_model: str, groq_model: str) -> Dict[str, Any]:
    if provider == "groq":
        return call_groq(context, scored, groq_model)
    if provider == "openai":
        return call_openai(context, scored, openai_model)
    return fallback_plan(context, scored, "No LLM provider configured. Set GROQ_API_KEY or OPENAI_API_KEY.")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Generate daily plan with Groq/OpenAI or local fallback.")
    parser.add_argument("--context", default=str(OUTPUT_DIR / "bond_advisor_context.json"))
    parser.add_argument("--scored", default=str(OUTPUT_DIR / "scored_methods.json"))
    parser.add_argument("--provider", default=os.getenv("ADVISOR_LLM_PROVIDER", "auto"), choices=["auto", "groq", "openai", "none"])
    parser.add_argument("--openai-model", default=DEFAULT_OPENAI_MODEL)
    parser.add_argument("--groq-model", default=DEFAULT_GROQ_MODEL)
    args = parser.parse_args()

    context = load_json(Path(args.context), default={}) or {}
    scored = load_json(Path(args.scored), default={}) or {}
    if not context:
        raise SystemExit("Missing context. Run scripts/build_context.py first.")
    if not scored:
        raise SystemExit("Missing scored methods. Run scripts/score_methods.py first.")

    provider = choose_provider(args.provider)
    plan = generate_plan(context, scored, provider, args.openai_model, args.groq_model)
    write_json(OUTPUT_DIR / "daily_plan.json", plan)
    (OUTPUT_DIR / "daily_plan.md").write_text(render_markdown(plan), encoding="utf-8")
    print(f"Provider: {provider}")
    print(f"Wrote {OUTPUT_DIR / 'daily_plan.json'}")
    print(f"Wrote {OUTPUT_DIR / 'daily_plan.md'}")


if __name__ == "__main__":
    main()
