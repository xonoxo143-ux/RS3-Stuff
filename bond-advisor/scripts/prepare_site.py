from __future__ import annotations

import shutil
from pathlib import Path

from _common import OUTPUT_DIR, PROJECT_ROOT, load_json, write_json

SITE_DIR = PROJECT_ROOT / "site"


def sanitize_plan() -> dict:
    plan = load_json(OUTPUT_DIR / "daily_plan.json", default={}) or {}
    allowed = {
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
    }
    return {key: value for key, value in plan.items() if key in allowed}


def main() -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    plan = sanitize_plan()
    write_json(SITE_DIR / "daily_plan.json", plan)

    daily_md = OUTPUT_DIR / "daily_plan.md"
    if daily_md.exists():
        shutil.copyfile(daily_md, SITE_DIR / "daily_plan.md")

    print(f"Prepared site output in {SITE_DIR}")


if __name__ == "__main__":
    main()
