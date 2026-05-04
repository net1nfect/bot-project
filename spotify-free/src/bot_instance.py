import asyncio
import time
from pathlib import Path

from config.settings import (
    COOKIES_DIR,
    PLAYLIST_CONFIG,
    RESTART_DELAY,
    SELECTORS,
    STREAM_LOG_INTERVAL,
    TRACK_PLAYBACK_CHECK,
)
from src.ad_handler import handle_ads, is_ad_visible
from src.browser_utils import close_browser, create_stealth_browser
from src.human_emulator import human_click, human_sleep
from src.utils import (
    get_playlist_config,
    generate_fingerprint,
    get_account_cookie_path,
    log_error,
    log_stream_event,
    parse_proxy_line,
)


class BotInstance:
    def __init__(self, account: dict):
        self.account = account
        self.proxy_config = parse_proxy_line(account.get("proxy", "")) or {}
        self.cookie_path = Path(account.get("cookie_file", "")) if account.get("cookie_file") else None
        self.fingerprint = account.get("fingerprint") or generate_fingerprint(account.get("email"))
        playlist_config = get_playlist_config()
        self.playlist_url = playlist_config.get("playlist_url")
        if not self.playlist_url:
            raise ValueError("Playlist URL must be configured in config/playlist.json")
        self.account_email = account.get("email", "unknown")
        self.last_stream_log = time.time()

    async def run(self) -> None:
        while True:
            try:
                await self._run_instance()
            except Exception as exc:
                log_error(f"Bot[{self.account_email}] crashed: {exc}")
                await asyncio.sleep(RESTART_DELAY)

    async def _run_instance(self) -> None:
        playwright = None
        browser = None
        try:
            playwright, browser, context = await create_stealth_browser(
                self.proxy_config,
                self.fingerprint,
                storage_state=str(self.cookie_path) if self.cookie_path and self.cookie_path.exists() else None,
            )
            page = await context.new_page()
            await page.goto(self.playlist_url, timeout=60000, wait_until="load")
            await human_sleep(3, 5)
            await self.accept_cookie_banner(page)
            await self.start_playback(page)
            await self.monitor_playback(page)
        finally:
            if browser and playwright:
                await close_browser(playwright, browser)

    async def accept_cookie_banner(self, page) -> None:
        cookie_selector = SELECTORS.get("cookie_accept")
        if cookie_selector:
            try:
                await human_click(page, cookie_selector)
                await human_sleep(1, 2)
            except Exception:
                pass

    async def start_playback(self, page) -> None:
        play_selector = SELECTORS.get("play_button")
        loop_selector = SELECTORS.get("loop_button")
        if play_selector:
            try:
                await human_click(page, play_selector)
                await human_sleep(2, 3)
            except Exception as exc:
                log_error(f"Bot[{self.account_email}] cannot click play: {exc}")
        if loop_selector:
            try:
                await human_click(page, loop_selector)
                await human_sleep(1, 2)
            except Exception:
                pass
        await self.mute_audio(page)

    async def mute_audio(self, page) -> None:
        await page.evaluate(
            "() => { const audio = document.querySelector('audio'); if (audio) { audio.muted = true; audio.volume = 0; } }"
        )

    async def get_playback_state(self, page) -> str:
        return await page.evaluate(
            '''() => {
                try {
                    const state = window.navigator.mediaSession?.playbackState;
                    if (state) return state;
                    const audio = document.querySelector('audio');
                    if (!audio) return 'stopped';
                    if (!audio.paused && audio.currentTime > 0) return 'playing';
                    if (audio.paused) return 'paused';
                } catch (e) {
                    return 'error';
                }
                return 'unknown';
            }'''
        )

    async def monitor_playback(self, page) -> None:
        while True:
            await asyncio.sleep(TRACK_PLAYBACK_CHECK)
            try:
                if await is_ad_visible(page):
                    await handle_ads(page, self.account_email)
                    continue
                state = await self.get_playback_state(page)
                if state == "playing":
                    now = time.time()
                    if now - self.last_stream_log >= STREAM_LOG_INTERVAL:
                        log_stream_event(f"Bot[{self.account_email}] streaming")
                        self.last_stream_log = now
                    continue
                if state in ("paused", "stopped", "unknown"):
                    await self.recover_playback(page)
                    continue
            except Exception as exc:
                log_error(f"Bot[{self.account_email}] monitoring exception: {exc}")
                raise

    async def recover_playback(self, page) -> None:
        play_selector = SELECTORS.get("play_button")
        if play_selector:
            try:
                await human_click(page, play_selector)
                await human_sleep(3, 5)
                log_stream_event(f"Bot[{self.account_email}] recovered playback")
            except Exception as exc:
                log_error(f"Bot[{self.account_email}] failed to recover playback: {exc}")
                raise
