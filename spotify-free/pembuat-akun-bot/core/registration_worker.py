"""Simulasi registrasi akun untuk analisis mekanisme validasi identitas.

Modul ini meniru perilaku pembuatan akun nyata dengan pengetikan manusia,
memeriksa pemicu CAPTCHA, dan menggunakan email sementara untuk verifikasi.
"""

from __future__ import annotations

import asyncio
import json
import random
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

import aiofiles
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from config import settings
from core.browser_factory import create_browser_session
from core.email_provider import MailGwProvider
from core.event_logger import EventLogger
from core.identity_generator import generate_identity
from core.session_manager import get_session_path


async def _type_like_human(page: Page, selector: str, text: str) -> None:
    field = page.locator(selector)
    await field.click()
    await field.fill("")

    for char in text:
        await field.type(char, delay=random.randint(50, 200))
        if random.random() < 0.08:
            await field.press("Backspace")
            await asyncio.sleep(random.uniform(0.05, 0.15))
            await field.type(char, delay=random.randint(50, 200))


async def _find_verification_link(provider: MailGwProvider, token: str, logger: EventLogger, worker_id: str) -> str:
    try:
        return await provider.get_verification_link(token)
    except Exception as exc:
        await logger.error(worker_id, "verification_link_error", {"error": str(exc)})
        raise


async def _save_result(result: Dict[str, Any]) -> None:
    session_file = settings.DATA_DIR / "sessions" / f"{result['id']}.json"
    session_file.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(session_file, "w", encoding="utf-8") as handle:
        await handle.write(json.dumps(result, ensure_ascii=False, indent=2))


async def run_registration_worker(
    worker_id: str,
    proxy: Optional[str],
    event_logger: EventLogger,
    headless: bool = True,
) -> Dict[str, Any]:
    """Menjalankan satu iterasi registrasi akun dengan email verifikasi."""
    identity = generate_identity()
    provider = MailGwProvider()
    email_address = ""
    email_token = ""
    account_id = ""
    browser_session = None
    start_ts = time.time()

    await event_logger.info(worker_id, "registration_start", {"identity": identity})

    try:
        email_address, email_token, account_id, email_password = await provider.create_account()
        await event_logger.info(worker_id, "email_account_created", {"email": email_address})

        browser_session = await create_browser_session(proxy=proxy, headless=headless)
        page = browser_session.page
        await page.goto("https://open.spotify.com/", timeout=60000)

        try:
            accept_button = page.locator(settings.SELECTORS.get("cookie_accept", ""))
            if await accept_button.is_visible():
                await accept_button.click()
        except PlaywrightTimeoutError:
            pass

        await page.wait_for_selector(settings.SELECTORS["signup_button"], timeout=30000)
        await page.click(settings.SELECTORS["signup_button"])

        await page.wait_for_selector(settings.SELECTORS["email_input"], timeout=30000)
        await _type_like_human(page, settings.SELECTORS["email_input"], email_address)
        await _type_like_human(page, settings.SELECTORS["password_input"], identity["password"])
        await _type_like_human(page, settings.SELECTORS["display_name_input"], identity["display_name"])

        day, month, year = identity["birthdate"].split("-")
        await _type_like_human(page, settings.SELECTORS["day_input"], day)
        await page.select_option(settings.SELECTORS["month_select"], value=str(int(month)))
        await _type_like_human(page, settings.SELECTORS["year_input"], year)

        gender_selector = settings.SELECTORS["gender_male"] if identity["gender"] == "male" else settings.SELECTORS["gender_female"]
        await page.click(gender_selector)
        await asyncio.sleep(random.uniform(0.5, 1.2))
        await page.click(settings.SELECTORS["submit_button"])

        await asyncio.sleep(random.uniform(5, 10))
        captcha_locator = page.locator("iframe[src*=captcha], div[class*=captcha], div[id*=captcha]")
        if await captcha_locator.count() > 0:
            await event_logger.detection(worker_id, "captcha_triggered", {"email": email_address, "proxy": proxy})
            status = "captcha"
        else:
            verification_link = await _find_verification_link(provider, email_token, event_logger, worker_id)
            await page.goto(verification_link, timeout=60000)
            await asyncio.sleep(random.uniform(3, 7))
            status = "verified"

        end_ts = time.time()
        result = {
            "id": f"{worker_id}_{uuid.uuid4().hex[:8]}",
            "email": email_address,
            "password": identity["password"],
            "username": identity["username"],
            "birthdate": identity["birthdate"],
            "proxy_used": proxy or "none",
            "user_agent_used": browser_session.user_agent if browser_session else "unknown",
            "captcha_triggered": status == "captcha",
            "registration_time_ms": int((end_ts - start_ts) * 1000),
            "status": status,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start_ts)),
        }

        await _save_result(result)
        await event_logger.info(worker_id, "registration_complete", result)

        if browser_session:
            storage_path = get_session_path(result["id"])
            await browser_session.context.storage_state(path=str(storage_path))
            await event_logger.info(worker_id, "storage_state_saved", {"session_file": str(storage_path)})

        return result
    except Exception as exc:
        await event_logger.error(worker_id, "registration_failed", {"error": str(exc), "proxy": proxy})
        raise
    finally:
        if browser_session:
            await browser_session.context.close()
            await browser_session.browser.close()
        if provider and account_id and email_token:
            await provider.delete_account(email_token, account_id)
        await provider.close()
