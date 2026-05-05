from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_TIMEOUT_SECONDS = 20

DEFAULT_USER_AGENT = os.getenv(
    "RS3_ADVISOR_USER_AGENT",
    "RS3-Bond-Advisor/0.2 (private account planning tool)",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Optional[Any] = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def load_manual_profile() -> Dict[str, Any]:
    return load_json(DATA_DIR / "manual_profile.json", default={}) or {}


def get_rsn(cli_rsn: Optional[str] = None) -> str:
    rsn = (cli_rsn or "").strip()
    if rsn:
        return rsn
    profile = load_manual_profile()
    rsn = str(profile.get("rsn", "")).strip()
    if not rsn:
        raise SystemExit("Missing RSN. Pass --rsn or fill data/manual_profile.json.")
    return rsn


def request_json(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    source: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json,text/plain,*/*",
    }
    if extra_headers:
        headers.update(extra_headers)

    fetched_at = now_iso()
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        payload: Dict[str, Any] = {
            "source": source,
            "url": response.url,
            "fetched_at": fetched_at,
            "status_code": response.status_code,
        }
        if not response.ok:
            payload.update(
                {
                    "status": "failed",
                    "confidence": "low",
                    "error": f"HTTP {response.status_code}",
                    "text_preview": response.text[:500],
                }
            )
            return payload
        try:
            data = response.json()
        except ValueError as exc:
            payload.update(
                {
                    "status": "invalid_json",
                    "confidence": "low",
                    "error": str(exc),
                    "text_preview": response.text[:500],
                }
            )
            return payload
        payload.update({"status": "available", "confidence": "medium_high", "data": data})
        return payload
    except requests.RequestException as exc:
        return {
            "source": source,
            "url": url,
            "fetched_at": fetched_at,
            "status": "failed",
            "confidence": "low",
            "error": str(exc),
        }


def request_text(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    source: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    headers = {"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/plain,*/*"}
    if extra_headers:
        headers.update(extra_headers)

    fetched_at = now_iso()
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        payload: Dict[str, Any] = {
            "source": source,
            "url": response.url,
            "fetched_at": fetched_at,
            "status_code": response.status_code,
        }
        if not response.ok:
            payload.update(
                {
                    "status": "failed",
                    "confidence": "low",
                    "error": f"HTTP {response.status_code}",
                    "text_preview": response.text[:500],
                }
            )
            return payload
        payload.update({"status": "available", "confidence": "high", "text": response.text})
        return payload
    except requests.RequestException as exc:
        return {
            "source": source,
            "url": url,
            "fetched_at": fetched_at,
            "status": "failed",
            "confidence": "low",
            "error": str(exc),
        }


def tagged_value(value: Any, source: str, status: str, confidence: str, notes: Optional[list[str]] = None) -> Dict[str, Any]:
    return {
        "value": value,
        "source": source,
        "status": status,
        "confidence": confidence,
        "notes": notes or [],
    }


def parse_price_to_int(value: Any) -> Optional[int]:
    """Parse ItemDB-style price values such as 12.3m, 897.2k, 1,234, or 0.

    Percent strings like '+27.0%' return None because they are trends, not prices.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = str(value).strip().lower().replace(",", "")
    if not text or text.endswith("%"):
        return None

    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")

    match = re.fullmatch(r"(\d+(?:\.\d+)?)([kmb])?", text)
    if not match:
        return None
    number = float(match.group(1))
    suffix = match.group(2)
    multiplier = {None: 1, "k": 1_000, "m": 1_000_000, "b": 1_000_000_000}[suffix]
    return int(sign * number * multiplier)


def compact_source_status(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source": payload.get("source"),
        "url": payload.get("url"),
        "fetched_at": payload.get("fetched_at"),
        "status": payload.get("status"),
        "status_code": payload.get("status_code"),
        "confidence": payload.get("confidence"),
        "error": payload.get("error"),
    }
