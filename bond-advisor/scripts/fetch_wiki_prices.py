from __future__ import annotations

import argparse
from typing import Any, Dict

from _common import DATA_DIR, OUTPUT_DIR, load_json, request_json, write_json

# This endpoint is attempted and validated, not treated as guaranteed.
# RS3 price data availability has shifted across community endpoints over time.
WIKI_RS_LATEST_URL = "https://prices.runescape.wiki/api/v1/rs/latest"
WIKI_RS_MAPPING_URL = "https://prices.runescape.wiki/api/v1/rs/mapping"


def load_watchlist() -> Dict[str, Any]:
    watchlist = load_json(DATA_DIR / "item_watchlist.json", default={}) or {}
    if not isinstance(watchlist, dict):
        raise SystemExit("data/item_watchlist.json must be a JSON object keyed by item ID.")
    return watchlist


def fetch_wiki_prices() -> Dict[str, Any]:
    watchlist = load_watchlist()
    latest = request_json(WIKI_RS_LATEST_URL, source="wiki_prices_rs_latest")
    mapping = request_json(WIKI_RS_MAPPING_URL, source="wiki_prices_rs_mapping")

    result: Dict[str, Any] = {
        "source": "wiki_prices_rs",
        "notes": [
            "This source is try-and-validate. If unavailable or invalid, use ItemDB as fallback.",
            "Do not assume these prices are instant buy/sell margins.",
        ],
        "latest_status": {
            "status": latest.get("status"),
            "status_code": latest.get("status_code"),
            "confidence": latest.get("confidence"),
            "error": latest.get("error"),
            "url": latest.get("url"),
        },
        "mapping_status": {
            "status": mapping.get("status"),
            "status_code": mapping.get("status_code"),
            "confidence": mapping.get("confidence"),
            "error": mapping.get("error"),
            "url": mapping.get("url"),
        },
        "items": {},
        "raw_latest": latest,
        "raw_mapping": mapping,
    }

    latest_data = latest.get("data")
    mapping_data = mapping.get("data")

    # Expected common shape is {"data": {"29492": {...}}}, but validate at runtime.
    latest_items = None
    if isinstance(latest_data, dict):
        latest_items = latest_data.get("data") if isinstance(latest_data.get("data"), dict) else latest_data

    mapping_items_by_id: Dict[str, Any] = {}
    if isinstance(mapping_data, list):
        for item in mapping_data:
            if isinstance(item, dict) and item.get("id") is not None:
                mapping_items_by_id[str(item["id"])] = item
    elif isinstance(mapping_data, dict):
        maybe_data = mapping_data.get("data")
        if isinstance(maybe_data, list):
            for item in maybe_data:
                if isinstance(item, dict) and item.get("id") is not None:
                    mapping_items_by_id[str(item["id"])] = item

    for item_id, metadata in watchlist.items():
        item_id_str = str(item_id)
        price_record = latest_items.get(item_id_str) if isinstance(latest_items, dict) else None
        result["items"][item_id_str] = {
            "watchlist_metadata": metadata,
            "mapping": mapping_items_by_id.get(item_id_str),
            "latest": price_record,
            "status": "available" if price_record is not None else "missing_or_unavailable",
            "confidence": "medium_high" if price_record is not None else "low",
        }

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Try fetching RuneScape Wiki RS price data for item_watchlist.json.")
    parser.parse_args()

    result = fetch_wiki_prices()
    write_json(OUTPUT_DIR / "wiki_prices_snapshot.json", result)
    print(f"Wrote {OUTPUT_DIR / 'wiki_prices_snapshot.json'}")


if __name__ == "__main__":
    main()
