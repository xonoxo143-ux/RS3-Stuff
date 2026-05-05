from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from _common import DATA_DIR, OUTPUT_DIR, compact_source_status, load_json, now_iso, tagged_value, write_json

SCRIPT_DIR = Path(__file__).resolve().parent


def run_fetch(script_name: str, args: list[str]) -> Dict[str, Any]:
    cmd = [sys.executable, str(SCRIPT_DIR / script_name), *args]
    proc = subprocess.run(cmd, cwd=str(SCRIPT_DIR.parent), capture_output=True, text=True)
    return {
        "script": script_name,
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "status": "ok" if proc.returncode == 0 else "failed",
    }


def load_snapshot(name: str) -> Dict[str, Any]:
    return load_json(OUTPUT_DIR / name, default={}) or {}


def extract_hiscores(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    parsed = snapshot.get("parsed") or {}
    skills = parsed.get("skills") or {}
    status = snapshot.get("status", "missing")
    confidence = snapshot.get("confidence", "low")
    return {
        "skills": tagged_value(skills, "hiscores", status, confidence),
        "source_status": compact_source_status(snapshot),
    }


def extract_profile(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    data = snapshot.get("data") if isinstance(snapshot.get("data"), dict) else {}
    summary = snapshot.get("summary") or {}
    status = snapshot.get("status", "missing")
    confidence = snapshot.get("confidence", "low")
    return {
        "summary": tagged_value(summary, "runemetrics_profile", status, confidence),
        "recent_activities": tagged_value(data.get("activities", []), "runemetrics_profile", status, confidence),
        "skillvalues": tagged_value(data.get("skillvalues", []), "runemetrics_profile", status, confidence),
        "source_status": compact_source_status(snapshot),
    }


def extract_quests(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    normalized = snapshot.get("normalized") or {}
    status = snapshot.get("status", "missing")
    confidence = snapshot.get("confidence", "low")
    return {
        "quests": tagged_value(normalized.get("quests", []), "runemetrics_quests", status, confidence),
        "summary": tagged_value(
            {
                "count": normalized.get("count", 0),
                "by_status": normalized.get("by_status", {}),
            },
            "runemetrics_quests",
            status,
            confidence,
            notes=["Falls back to manual unlock flags if unavailable."],
        ),
        "source_status": compact_source_status(snapshot),
    }


def extract_itemdb(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    items_out: Dict[str, Any] = {}
    for item_id, record in (snapshot.get("items") or {}).items():
        detail = record.get("detail") or {}
        graph = record.get("graph") or {}
        normalized = detail.get("normalized") or {}
        items_out[item_id] = {
            "metadata": record.get("watchlist_metadata", {}),
            "detail": tagged_value(
                normalized,
                "itemdb_detail",
                detail.get("status", "missing"),
                detail.get("confidence", "low"),
            ),
            "graph_summary": tagged_value(
                graph.get("summary", {}),
                "itemdb_graph",
                graph.get("status", "missing"),
                graph.get("confidence", "low"),
            ),
        }
    return {
        "info": snapshot.get("info", {}),
        "items": items_out,
    }


def extract_wiki_prices(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    items_out: Dict[str, Any] = {}
    for item_id, record in (snapshot.get("items") or {}).items():
        items_out[item_id] = {
            "metadata": record.get("watchlist_metadata", {}),
            "mapping": record.get("mapping"),
            "latest": tagged_value(
                record.get("latest"),
                "wiki_prices_rs_latest",
                record.get("status", "missing"),
                record.get("confidence", "low"),
                notes=["Try-and-validate source. Use ItemDB fallback if unavailable."],
            ),
        }
    return {
        "latest_status": snapshot.get("latest_status", {}),
        "mapping_status": snapshot.get("mapping_status", {}),
        "items": items_out,
    }


def get_bond_price(itemdb_context: Dict[str, Any], manual_profile: Dict[str, Any]) -> Dict[str, Any]:
    manual_target = manual_profile.get("bond_target_price")
    if manual_target:
        return tagged_value(manual_target, "manual_profile", "available", "medium", ["Manual override."])

    bond = ((itemdb_context.get("items") or {}).get("29492") or {}).get("detail") or {}
    value = (bond.get("value") or {}).get("current_gp")
    status = bond.get("status", "missing")
    confidence = bond.get("confidence", "low")
    return tagged_value(value, "itemdb_detail", status, confidence, ["Bond item ID 29492."])


def build_context(run_fetchers: bool, rsn: Optional[str], mode: str) -> Dict[str, Any]:
    fetch_runs = []
    fetch_args = []
    if rsn:
        fetch_args.extend(["--rsn", rsn])

    if run_fetchers:
        fetch_runs.append(run_fetch("fetch_hiscores.py", [*fetch_args, "--mode", mode]))
        fetch_runs.append(run_fetch("fetch_runemetrics_profile.py", fetch_args))
        fetch_runs.append(run_fetch("fetch_runemetrics_quests.py", fetch_args))
        fetch_runs.append(run_fetch("fetch_itemdb.py", []))
        fetch_runs.append(run_fetch("fetch_wiki_prices.py", []))

    manual_profile = load_json(DATA_DIR / "manual_profile.json", default={}) or {}
    method_catalog = load_json(DATA_DIR / "method_catalog.json", default={}) or {}
    item_watchlist = load_json(DATA_DIR / "item_watchlist.json", default={}) or {}
    actual_results_log = load_json(DATA_DIR / "actual_results_log.json", default={}) or {}

    hiscores = extract_hiscores(load_snapshot("hiscores_snapshot.json"))
    profile = extract_profile(load_snapshot("runemetrics_profile_snapshot.json"))
    quests = extract_quests(load_snapshot("runemetrics_quests_snapshot.json"))
    itemdb = extract_itemdb(load_snapshot("itemdb_snapshot.json"))
    wiki_prices = extract_wiki_prices(load_snapshot("wiki_prices_snapshot.json"))
    bond_price = get_bond_price(itemdb, manual_profile)

    days = 14
    safe_days = 12
    bond_value = bond_price.get("value")
    daily_target = int(bond_value / days) if isinstance(bond_value, int) and bond_value > 0 else None
    safe_daily_target = int(bond_value / safe_days) if isinstance(bond_value, int) and bond_value > 0 else None

    context = {
        "schema_version": "0.3",
        "built_at": now_iso(),
        "fetch_runs": fetch_runs,
        "manual_profile": manual_profile,
        "character": {
            "rsn": rsn or manual_profile.get("rsn"),
            "hiscores": hiscores,
            "runemetrics_profile": profile,
            "runemetrics_quests": quests,
            "manual_unlocks": manual_profile.get("important_unlocks", {}),
            "gear_summary": manual_profile.get("gear_summary", {}),
            "preferences": {
                "available_playtime_per_day_minutes": manual_profile.get("available_playtime_per_day_minutes"),
                "preferred_attention": manual_profile.get("preferred_attention"),
                "mobile_only": manual_profile.get("mobile_only"),
                "combat_comfort": manual_profile.get("combat_comfort", {}),
                "methods_to_avoid": manual_profile.get("methods_to_avoid", []),
                "methods_you_like": manual_profile.get("methods_you_like", []),
            },
            "bank_notes": manual_profile.get("bank_notes", {}),
            "coins": tagged_value(manual_profile.get("coins"), "manual_profile", "manual", "medium"),
        },
        "market": {
            "bond_price": bond_price,
            "daily_target_gp": tagged_value(daily_target, "calculated", "available" if daily_target else "missing", "medium"),
            "safe_daily_target_gp": tagged_value(safe_daily_target, "calculated", "available" if safe_daily_target else "missing", "medium", ["Uses 12 days instead of 14 for buffer."]),
            "item_watchlist": item_watchlist,
            "itemdb": itemdb,
            "wiki_prices": wiki_prices,
        },
        "methods": method_catalog,
        "actual_results_log": actual_results_log,
        "uncertainties": [],
    }

    if quests["summary"]["status"] != "available":
        context["uncertainties"].append("RuneMetrics quest data unavailable or invalid. Use manual unlock flags.")
    if wiki_prices.get("latest_status", {}).get("status") != "available":
        context["uncertainties"].append("Wiki RS prices unavailable or invalid. Use ItemDB as price fallback.")
    if not safe_daily_target:
        context["uncertainties"].append("Bond price unavailable. Daily target cannot be calculated.")

    return context


def main() -> None:
    parser = argparse.ArgumentParser(description="Build merged RS3 bond advisor context JSON.")
    parser.add_argument("--rsn", default=None, help="RuneScape display name. Overrides manual_profile.json for this run.")
    parser.add_argument("--mode", default="normal", choices=["normal", "ironman", "hardcore_ironman"], help="Hiscores table.")
    parser.add_argument("--skip-fetch", action="store_true", help="Use existing output snapshots instead of fetching.")
    args = parser.parse_args()

    context = build_context(run_fetchers=not args.skip_fetch, rsn=args.rsn, mode=args.mode)
    write_json(OUTPUT_DIR / "bond_advisor_context.json", context)
    print(f"Wrote {OUTPUT_DIR / 'bond_advisor_context.json'}")


if __name__ == "__main__":
    main()
