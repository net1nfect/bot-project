"""Simulator aktivitas pemutaran untuk menguji deteksi anomali dan antisipasi sistem.

Modul ini memuat sesi browser yang sudah terautentikasi dan mensimulasikan
interaksi pengguna yang realistis pada halaman playlist.
"""

from __future__ import annotations

import asyncio
import random
import time
from typing import Dict, Optional

from core.browser_factory import BrowserSession, create_browser_session
from core.event_logger import EventLogger
from core.session_manager import load_session_state
from config import settings


async def _natural_scroll(page) -> None:
    for _ in range(random.randint(2, 5)):
        y_offset = random.randint(200, 500)
        await page.mouse.wheel(0, y_offset)
        await asyncio.sleep(random.uniform(0.5, 1.5))


async def _click_if_visible(page, selector: str) -> bool:
    locator = page.locator(selector)
    if await locator.count() and await locator.is_visible():
        await locator.click()
        return True
    return False


async def _parse_playback_state(page) -> str:
    try:
        state = await page.evaluate("() => navigator.mediaSession?.playbackState || 'unknown'")
    except Exception:
        state = "unknown"
    return state


async def simulate_playback(
    worker_id: str,
    session_id: str,
    playlist_url: str,
    event_logger: EventLogger,
    duration_seconds: int = 180,
    proxy: Optional[str] = None,
    headless: bool = True,
) -> None:
    """Jalankan pengujian pemutaran dengan sesi yang sudah dipulihkan."""
    session_path = load_session_state(session_id)
    if session_path is None:
        await event_logger.error(worker_id, "playback_missing_session", {"session_id": session_id})
        return

    browser_session: Optional[BrowserSession] = None
    await event_logger.info(worker_id, "playback_start", {"session_id": session_id, "playlist_url": playlist_url})

    try:
        browser_session = await create_browser_session(proxy=proxy, storage_state=session_path, headless=headless)
        page = browser_session.page
        await page.goto(playlist_url, timeout=60000)
        await asyncio.sleep(random.uniform(3, 8))
        await _natural_scroll(page)

        clicked = await _click_if_visible(page, settings.SELECTORS["play_button"])
        if not clicked:
            await event_logger.warning(worker_id, "play_button_not_found", {"session_id": session_id})

        await _click_if_visible(page, settings.SELECTORS["loop_button"])
        await asyncio.sleep(random.uniform(2, 4))

        start_ts = time.time()
        last_state = await _parse_playback_state(page)
        await event_logger.info(worker_id, "playback_state", {"state": last_state})

        while time.time() - start_ts < duration_seconds:
            await asyncio.sleep(15)
            state = await _parse_playback_state(page)
            if state != last_state:
                await event_logger.info(worker_id, "playback_state_change", {"from": last_state, "to": state})
                last_state = state

            if state == "paused":
                ad_visible = await page.locator("[aria-label*='Ad'], [data-testid*='ad']").count()
                if ad_visible:
                    await event_logger.info(worker_id, "ad_detected", {"session_id": session_id})
                    await asyncio.sleep(random.uniform(15, 30))
                else:
                    await event_logger.warning(worker_id, "playback_paused", {"session_id": session_id})
                    await _click_if_visible(page, settings.SELECTORS["play_button"])

            if random.random() < 0.1:
                await _click_if_visible(page, "button[aria-label*='Save'], button[aria-label*='Like']")
                await asyncio.sleep(random.uniform(1, 2))

        await event_logger.info(worker_id, "playback_complete", {"session_id": session_id, "duration": duration_seconds})
    except Exception as exc:
        await event_logger.error(worker_id, "playback_error", {"error": str(exc), "session_id": session_id})
        raise
    finally:
        if browser_session:
            await browser_session.context.close()
            await browser_session.browser.close()
