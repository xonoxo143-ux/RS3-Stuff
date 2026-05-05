from __future__ import annotations

import argparse
import csv
import io
from typing import Any, Dict, List

from _common import OUTPUT_DIR, get_rsn, request_text, write_json

HISCORES_URLS = {
    "normal": "https://secure.runescape.com/m=hiscore/index_lite.ws",
    "ironman": "https://secure.runescape.com/m=hiscore_ironman/index_lite.ws",
    "hardcore_ironman": "https://secure.runescape.com/m=hiscore_hardcore_ironman/index_lite.ws",
}

# RS3 hiscores order. Later rows are activities/minigames and can change more often.
SKILL_NAMES = [
    "overall",
    "attack",
    "defence",
    "strength",
    "constitution",
    "ranged",
    "prayer",
    "magic",
    "cooking",
    "woodcutting",
    "fletching",
    "fishing",
    "firemaking",
    "crafting",
    "smithing",
    "mining",
    "herblore",
    "agility",
    "thieving",
    "slayer",
    "farming",
    "runecrafting",
    "hunter",
    "construction",
    "summoning",
    "dungeoneering",
    "divination",
    "invention",
    "archaeology",
    "necromancy",
]


def parse_hiscores_csv(text: str) -> Dict[str, Any]:
    rows = list(csv.reader(io.StringIO(text.strip())))
    skills: Dict[str, Dict[str, int]] = {}
    extras: List[List[str]] = []

    for index, row in enumerate(rows):
        if index < len(SKILL_NAMES):
            if len(row) < 3:
                continue
            rank, level, xp = row[:3]
            skills[SKILL_NAMES[index]] = {
                "rank": int(rank),
                "level": int(level),
                "xp": int(xp),
            }
        else:
            extras.append(row)

    return {
        "skills": skills,
        "extra_rows": extras,
        "raw_row_count": len(rows),
    }


def fetch_hiscores(rsn: str, mode: str) -> Dict[str, Any]:
    url = HISCORES_URLS[mode]
    payload = request_text(url, params={"player": rsn}, source=f"hiscores_{mode}")
    if payload.get("status") == "available":
        try:
            payload["parsed"] = parse_hiscores_csv(payload["text"])
            payload["confidence"] = "high"
        except Exception as exc:  # deliberately broad: endpoint shape can change
            payload.update(
                {
                    "status": "parse_failed",
                    "confidence": "low",
                    "error": str(exc),
                }
            )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch RS3 hiscores data.")
    parser.add_argument("--rsn", default=None, help="RuneScape display name. Defaults to data/manual_profile.json.")
    parser.add_argument(
        "--mode",
        choices=sorted(HISCORES_URLS),
        default="normal",
        help="Hiscores table to query.",
    )
    args = parser.parse_args()

    rsn = get_rsn(args.rsn)
    result = fetch_hiscores(rsn, args.mode)
    result["rsn"] = rsn
    result["mode"] = args.mode
    write_json(OUTPUT_DIR / "hiscores_snapshot.json", result)
    print(f"Wrote {OUTPUT_DIR / 'hiscores_snapshot.json'}")


if __name__ == "__main__":
    main()
