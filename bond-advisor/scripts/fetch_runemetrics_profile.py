from __future__ import annotations

import argparse
from typing import Any, Dict

from _common import OUTPUT_DIR, get_rsn, request_json, write_json

RUNEMETRICS_PROFILE_URL = "https://apps.runescape.com/runemetrics/profile/profile"


def fetch_runemetrics_profile(rsn: str, activities: int = 20) -> Dict[str, Any]:
    payload = request_json(
        RUNEMETRICS_PROFILE_URL,
        params={"user": rsn, "activities": activities},
        source="runemetrics_profile",
    )

    data = payload.get("data")
    if payload.get("status") == "available":
        if isinstance(data, dict) and data.get("error"):
            payload.update(
                {
                    "status": "unavailable",
                    "confidence": "low",
                    "error": data.get("error"),
                }
            )
        elif isinstance(data, dict):
            payload["confidence"] = "high"
            payload["summary"] = {
                "name": data.get("name"),
                "combatlevel": data.get("combatlevel"),
                "totalskill": data.get("totalskill"),
                "totalxp": data.get("totalxp"),
                "questsstarted": data.get("questsstarted"),
                "questscomplete": data.get("questscomplete"),
                "questsnotstarted": data.get("questsnotstarted"),
                "activities_count": len(data.get("activities", []) or []),
                "skillvalues_count": len(data.get("skillvalues", []) or []),
            }
        else:
            payload.update(
                {
                    "status": "invalid_shape",
                    "confidence": "low",
                    "error": "Expected JSON object from RuneMetrics profile.",
                }
            )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch RuneMetrics public profile data.")
    parser.add_argument("--rsn", default=None, help="RuneScape display name. Defaults to data/manual_profile.json.")
    parser.add_argument("--activities", type=int, default=20, help="Number of recent activity entries to request.")
    args = parser.parse_args()

    rsn = get_rsn(args.rsn)
    result = fetch_runemetrics_profile(rsn, args.activities)
    result["rsn"] = rsn
    write_json(OUTPUT_DIR / "runemetrics_profile_snapshot.json", result)
    print(f"Wrote {OUTPUT_DIR / 'runemetrics_profile_snapshot.json'}")


if __name__ == "__main__":
    main()
