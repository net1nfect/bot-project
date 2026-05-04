import asyncio
from datetime import datetime, timezone

from config.settings import SELECTORS, AD_MAX_WAIT_SECONDS
from src.human_emulator import human_sleep, human_click
from src.utils import log_stream_event, log_error


async def is_ad_visible(page) -> bool:
    ad_selector = SELECTORS.get("ad_playing")
    if ad_selector and await page.query_selector(ad_selector):
        return True
    return await page.evaluate(
        "() => !!document.querySelector('[data-testid*=\"ad\"]') || !!document.querySelector('[class*=\"ad\"]')"
    )


async def is_skip_button_present(page) -> bool:
    skip_selector = SELECTORS.get("skip_ad_button")
    if skip_selector and await page.query_selector(skip_selector):
        return True
    return False


async def handle_ads(page, account_email: str) -> None:
    start = datetime.now(timezone.utc)
    log_stream_event(f"{account_email} | Ad detected - waiting")
    deadline = start.timestamp() + AD_MAX_WAIT_SECONDS
    while datetime.now(timezone.utc).timestamp() < deadline:
        if await is_skip_button_present(page):
            try:
                await human_click(page, SELECTORS.get("skip_ad_button"))
                log_stream_event(f"{account_email} | Skip button clicked")
                await human_sleep(2, 3)
                break
            except Exception as error:
                log_error(f"Ad skip click failed: {error}")
        if not await is_ad_visible(page):
            log_stream_event(f"{account_email} | Ad finished")
            break
        await human_sleep(3, 4)

    if await is_ad_visible(page):
        log_stream_event(f"{account_email} | Ad timeout reached, resuming playback")
        await resume_playback(page, account_email)


async def resume_playback(page, account_email: str) -> None:
    try:
        play_selector = SELECTORS.get("play_button")
        if play_selector and await page.query_selector(play_selector):
            await human_click(page, play_selector)
            await human_sleep(2, 4)
            log_stream_event(f"{account_email} | Playback resumed after ad")
    except Exception as exc:
        log_error(f"Failed to resume playback for {account_email}: {exc}")
