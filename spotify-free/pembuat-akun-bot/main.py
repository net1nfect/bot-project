"""Orkestrator utama eksperimen untuk koordinasi worker registrasi dan pemutaran."""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import dataclass
from itertools import cycle
from typing import Any, Dict, List, Optional

from config import settings
from core.event_logger import EventLogger
from core.playback_simulator import simulate_playback
from core.registration_worker import run_registration_worker


@dataclass
class WorkerStats:
    active_workers: int = 0
    total_attempts: int = 0
    total_success: int = 0
    total_failures: int = 0
    total_errors: int = 0


class ExperimentOrchestrator:
    def __init__(self, mode: str, worker_count: int, playlist_url: Optional[str], headless: bool = True) -> None:
        self.mode = mode
        self.worker_count = worker_count
        self.playlist_url = playlist_url or settings.TARGET_PLAYLIST_URL
        self.headless = headless
        self.event_logger = EventLogger()
        self.stats = WorkerStats()
        self._lock = asyncio.Lock()
        self._stop_event = asyncio.Event()
        self.proxies = settings.PROXY_ADDRESSES or [None]

    async def _update_stats(self, field: str, delta: int = 1) -> None:
        async with self._lock:
            setattr(self.stats, field, getattr(self.stats, field) + delta)

    async def _report_loop(self) -> None:
        while not self._stop_event.is_set():
            await asyncio.sleep(settings.HEALTH_CHECK_INTERVAL)
            await self.event_logger.info(
                "orchestrator",
                "health_report",
                {
                    "active_workers": self.stats.active_workers,
                    "total_attempts": self.stats.total_attempts,
                    "total_success": self.stats.total_success,
                    "total_failures": self.stats.total_failures,
                    "total_errors": self.stats.total_errors,
                },
            )

    async def _worker_loop(self, worker_index: int, proxy: Optional[str]) -> None:
        proxy_user = proxy or "none"
        worker_id = f"worker_{worker_index:02d}"
        while not self._stop_event.is_set():
            await self._update_stats("active_workers", 1)
            try:
                await self.event_logger.info(worker_id, "worker_cycle_start", {"proxy": proxy_user, "mode": self.mode})
                if self.mode == "registration":
                    result = await run_registration_worker(worker_id, proxy, self.event_logger, headless=self.headless)
                    if result["status"] == "verified":
                        await self._update_stats("total_success")
                    else:
                        await self._update_stats("total_failures")
                else:
                    assert self.playlist_url is not None
                    await simulate_playback(worker_id, f"session_{worker_index}", self.playlist_url, self.event_logger, proxy=proxy, headless=self.headless)
                    await self._update_stats("total_success")
            except Exception as exc:
                await self.event_logger.error(worker_id, "worker_exception", {"error": str(exc)})
                await self._update_stats("total_errors")
                await self._update_stats("total_failures")
                await asyncio.sleep(settings.RESTART_DELAY_SECONDS)
            finally:
                await self._update_stats("active_workers", -1)
                await self._update_stats("total_attempts")

    async def run(self) -> None:
        proxis: List[Optional[str]] = list(self.proxies)
        if not proxis:
            proxis = [None]

        tasks: List[asyncio.Task[Any]] = []
        for index, proxy in zip(range(self.worker_count), cycle(proxis)):
            tasks.append(asyncio.create_task(self._worker_loop(index + 1, proxy)))

        tasks.append(asyncio.create_task(self._report_loop()))

        await self.event_logger.info("orchestrator", "experiment_started", {"mode": self.mode, "worker_count": self.worker_count})

        await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

    def stop(self) -> None:
        self._stop_event.set()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Orkestrator eksperimen pertahanan platform streaming")
    parser.add_argument("--mode", choices=["registration", "playback"], default="registration")
    parser.add_argument("--workers", type=int, default=settings.MAX_CONCURRENT_WORKERS)
    parser.add_argument("--playlist-url", type=str, default=settings.TARGET_PLAYLIST_URL)
    parser.add_argument("--headless", action="store_true", default=True, help="Jalankan browser dalam mode headless (tanpa GUI)")
    parser.add_argument("--visual", action="store_true", help="Jalankan browser dengan GUI untuk monitoring (override --headless)")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    headless = not args.visual  # --visual override headless
    orchestrator = ExperimentOrchestrator(mode=args.mode, worker_count=args.workers, playlist_url=args.playlist_url, headless=headless)
    try:
        asyncio.run(orchestrator.run())
    except KeyboardInterrupt:
        orchestrator.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
