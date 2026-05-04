"""Pencatat peristiwa eksperimen untuk audit dan analisis forensik."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

from config import settings


class EventLogger:
    """Logger terstruktur dengan rotasi file setiap 10MB."""

    def __init__(self, log_name: str = "experiment.log") -> None:
        self.log_path = settings.LOG_DIR / log_name
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger("spotify_defense_analysis")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            handler = RotatingFileHandler(
                filename=self.log_path,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    async def log(
        self,
        level: str,
        worker_id: str,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "level": level,
            "worker_id": worker_id,
            "event_type": event_type,
            "payload": payload or {},
        }
        message = json.dumps(entry, ensure_ascii=False)
        await asyncio.to_thread(self._logger.info, message)

    async def info(self, worker_id: str, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        await self.log("INFO", worker_id, event_type, payload)

    async def warning(self, worker_id: str, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        await self.log("WARNING", worker_id, event_type, payload)

    async def error(self, worker_id: str, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        await self.log("ERROR", worker_id, event_type, payload)

    async def detection(self, worker_id: str, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        await self.log("DETECTION", worker_id, event_type, payload)
