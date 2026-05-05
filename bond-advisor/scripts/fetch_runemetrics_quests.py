from __future__ import annotations

import argparse
from typing import Any, Dict

from _common import OUTPUT_DIR, get_rsn, request_json, write_json

RUNEMETRICS_QUESTS_URL = "https://apps.runescape.com/runemetrics/quests"


def normalize_quests(data: Any) -> Dict[str, Any]:
    if isinstance(data, dict) and isinstance(data.get("quests"), list):
        quests = data["quests"]
    elif isinstance(data, list):
        quests = data
    else:
        return {"valid": False, "quests": [], "error": "Expected quests array or object containing quests array."}

    by_status: Dict[str, int] = {}
    normalized = []
    for quest in quests:
        if not isinstance(quest, dict):
            continue
        status = str(quest.get("status", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
        normalized.append(
            {
                "title": quest.get("title"),
                "status": status,
                "difficulty": quest.get("difficulty"),
                "members": quest.get("members"),
                "quest_points": quest.get("questPoints"),
                "user_eligible": quest.get("userEligible"),
            }
        )

    return {
        "valid": True,
        "count": len(normalized),
        "by_status": by_status,
        "quests": normalized,
    }


def fetch_runemetrics_quests(rsn: str) -> Dict[str, Any]:
    payload = request_json(
        RUNEMETRICS_QUESTS_URL,
        params={"user": rsn},
        source="runemetrics_quests",
    )

    if payload.get("status") == "available":
        data = payload.get("data")
        if isinstance(data, dict) and data.get("error"):
            payload.update(
                {
                    "status": "unavailable",
                    "confidence": "low",
                    "error": data.get("error"),
                }
            )
        else:
            normalized = normalize_quests(data)
            payload["normalized"] = normalized
            if normalized.get("valid") and normalized.get("count", 0) > 0:
                payload["confidence"] = "high"
            else:
                payload.update(
                    {
                        "status": "invalid_or_empty",
                        "confidence": "low",
                        "error": normalized.get("error", "Quest endpoint returned no usable quests."),
                    }
                )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch RuneMetrics public quest data.")
    parser.add_argument("--rsn", default=None, help="RuneScape display name. Defaults to data/manual_profile.json.")
    args = parser.parse_args()

    rsn = get_rsn(args.rsn)
    result = fetch_runemetrics_quests(rsn)
    result["rsn"] = rsn
    write_json(OUTPUT_DIR / "runemetrics_quests_snapshot.json", result)
    print(f"Wrote {OUTPUT_DIR / 'runemetrics_quests_snapshot.json'}")


if __name__ == "__main__":
    main()
