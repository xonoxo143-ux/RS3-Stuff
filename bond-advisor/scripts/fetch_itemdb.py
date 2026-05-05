from __future__ import annotations

import argparse
from typing import Any, Dict

from _common import DATA_DIR, OUTPUT_DIR, load_json, parse_price_to_int, request_json, write_json

ITEMDB_INFO_URL = "https://secure.runescape.com/m=itemdb_rs/api/info.json"
ITEMDB_DETAIL_URL = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/detail.json"
ITEMDB_GRAPH_URL_TEMPLATE = "https://secure.runescape.com/m=itemdb_rs/api/graph/{item_id}.json"


def load_watchlist() -> Dict[str, Any]:
    watchlist = load_json(DATA_DIR / "item_watchlist.json", default={}) or {}
    if not isinstance(watchlist, dict):
        raise SystemExit("data/item_watchlist.json must be a JSON object keyed by item ID.")
    return watchlist


def fetch_item_detail(item_id: str) -> Dict[str, Any]:
    payload = request_json(
        ITEMDB_DETAIL_URL,
        params={"item": item_id},
        source="itemdb_detail",
    )
    if payload.get("status") == "available":
        item = (payload.get("data") or {}).get("item")
        if not isinstance(item, dict):
            payload.update(
                {
                    "status": "invalid_shape",
                    "confidence": "low",
                    "error": "Expected data.item object from ItemDB detail.",
                }
            )
        else:
            current = item.get("current") or {}
            today = item.get("today") or {}
            payload["normalized"] = {
                "id": item_id,
                "name": item.get("name"),
                "description": item.get("description"),
                "members": item.get("members"),
                "current_raw": current.get("price"),
                "current_gp": parse_price_to_int(current.get("price")),
                "current_trend": current.get("trend"),
                "today_raw": today.get("price"),
                "today_gp": parse_price_to_int(today.get("price")),
                "today_trend": today.get("trend"),
                "day30_raw": item.get("day30", {}).get("change"),
                "day90_raw": item.get("day90", {}).get("change"),
                "day180_raw": item.get("day180", {}).get("change"),
                "icon": item.get("icon"),
                "icon_large": item.get("icon_large"),
            }
            payload["confidence"] = "medium_high"
    return payload


def fetch_item_graph(item_id: str) -> Dict[str, Any]:
    payload = request_json(
        ITEMDB_GRAPH_URL_TEMPLATE.format(item_id=item_id),
        source="itemdb_graph",
    )
    if payload.get("status") == "available":
        data = payload.get("data") or {}
        daily = data.get("daily") if isinstance(data, dict) else None
        average = data.get("average") if isinstance(data, dict) else None
        if not isinstance(daily, dict) or not isinstance(average, dict):
            payload.update(
                {
                    "status": "invalid_shape",
                    "confidence": "low",
                    "error": "Expected daily and average graph objects.",
                }
            )
        else:
            latest_daily_key = max(daily.keys(), default=None)
            latest_average_key = max(average.keys(), default=None)
            payload["summary"] = {
                "daily_points": len(daily),
                "average_points": len(average),
                "latest_daily_timestamp": latest_daily_key,
                "latest_daily_gp": daily.get(latest_daily_key) if latest_daily_key else None,
                "latest_average_timestamp": latest_average_key,
                "latest_average_gp": average.get(latest_average_key) if latest_average_key else None,
            }
            payload["confidence"] = "medium_high"
    return payload


def fetch_itemdb(include_graphs: bool = True) -> Dict[str, Any]:
    watchlist = load_watchlist()
    result: Dict[str, Any] = {
        "source": "itemdb",
        "watchlist_count": len(watchlist),
        "info": request_json(ITEMDB_INFO_URL, source="itemdb_info"),
        "items": {},
    }

    for item_id, metadata in watchlist.items():
        item_record: Dict[str, Any] = {
            "watchlist_metadata": metadata,
            "detail": fetch_item_detail(str(item_id)),
        }
        if include_graphs:
            item_record["graph"] = fetch_item_graph(str(item_id))
        result["items"][str(item_id)] = item_record
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch ItemDB detail and graph data for item_watchlist.json.")
    parser.add_argument("--no-graphs", action="store_true", help="Skip graph endpoints.")
    args = parser.parse_args()

    result = fetch_itemdb(include_graphs=not args.no_graphs)
    write_json(OUTPUT_DIR / "itemdb_snapshot.json", result)
    print(f"Wrote {OUTPUT_DIR / 'itemdb_snapshot.json'}")


if __name__ == "__main__":
    main()
