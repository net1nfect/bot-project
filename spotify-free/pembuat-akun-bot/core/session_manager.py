"""Manajemen sesi penyimpanan browser untuk menghindari deteksi pada login berulang.

Modul ini menyimpan dan memuat storage_state Playwright untuk rotasi sesi.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from config import settings


def _ensure_directories() -> None:
    settings.SESSION_DIR.mkdir(parents=True, exist_ok=True)


def get_session_path(session_id: str) -> Path:
    _ensure_directories()
    return settings.SESSION_DIR / f"{session_id}.json"


def save_session_state_path(session_id: str) -> Path:
    return get_session_path(session_id)


def session_exists(session_id: str) -> bool:
    return get_session_path(session_id).is_file()


def list_sessions() -> List[str]:
    _ensure_directories()
    return [path.stem for path in settings.SESSION_DIR.glob("*.json")]


def cleanup_session(session_id: str) -> None:
    session_file = get_session_path(session_id)
    if session_file.exists():
        session_file.unlink(missing_ok=True)


def load_session_state(session_id: str) -> Optional[Path]:
    path = get_session_path(session_id)
    return path if path.exists() else None


def parse_storage_state(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
