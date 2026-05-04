import argparse
import asyncio
import random
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import Page

from config.settings import PROXY_FILE
from src.browser_utils import close_browser, create_stealth_browser
from src.human_emulator import click_if_visible, human_sleep, human_type
from src.temp_mail import create_temp_email, get_verification_link
from src.utils import (
    ACCOUNTS_FILE,
    ensure_directories,
    build_profile,
    generate_fingerprint,
    load_accounts,
    log_account_event,
    log_error,
    parse_proxy_line,
    save_accounts,
)

SIGNUP_URL = "https://www.spotify.com/signup"


def load_proxies() -> list[dict]:
    path = Path(PROXY_FILE)
    if not path.exists():
        raise FileNotFoundError(f"Proxy file not found: {path}")
    proxies = []
    for line in path.read_text(encoding="utf-8").splitlines():
        proxy = parse_proxy_line(line)
        if proxy:
            proxies.append(proxy)
    if not proxies:
        raise RuntimeError("No valid proxies found in proxies.txt")
    return proxies


async def safe_fill(page: Page, selectors: list[str], text: str) -> bool:
    for selector in selectors:
        element = await page.query_selector(selector)
        if element:
            await element.fill("")
            await human_type(page, selector, text)
            return True
    return False


async def detect_captcha(page: Page) -> bool:
    if await page.query_selector('iframe[src*="recaptcha"]'):
        return True
    if await page.query_selector('div[id*="captcha"], div[class*="captcha"]'):
        return True
    return False


async def submit_signup(page: Page) -> bool:
    if await click_if_visible(page, 'button[type="submit"]'):
        return True
    if await click_if_visible(page, 'button[data-testid="register-button"]'):
        return True
    return False


async def create_account(proxy: dict, profile: dict) -> dict | None:
    fingerprint = generate_fingerprint()
    playwright = None
    browser = None
    try:
        playwright, browser, context = await create_stealth_browser(proxy, fingerprint)
        page = await context.new_page()
        await page.goto(SIGNUP_URL, timeout=60000, wait_until="networkidle")
        await human_sleep(2, 4)

        await click_if_visible(page, 'button[id="onetrust-accept-btn-handler"]')
        await human_sleep(1, 2)

        if not await safe_fill(page, [
            'input[name="email"]',
            'input[id="email"]',
            'input[name="username"]',
        ], profile["email"]):
            raise RuntimeError("Signup email input not found")

        await safe_fill(page, [
            'input[name="confirm_email"]',
            'input[name="confirm-email"]',
            'input[id="confirm-email"]',
        ], profile["email"])
        await safe_fill(page, [
            'input[name="password"]',
            'input[id="password"]',
        ], profile["password"])
        await safe_fill(page, [
            'input[name="displayname"]',
            'input[name="name"]',
            'input[id="display-name"]',
        ], profile["display_name"])

        await safe_fill(page, [
            'select[name="month"]',
            'select[id="month"]',
            'input[name="month"]',
        ], str(profile["birth_month"]))
        await safe_fill(page, [
            'select[name="day"]',
            'select[id="day"]',
            'input[name="day"]',
        ], str(profile["birth_day"]))
        await safe_fill(page, [
            'select[name="year"]',
            'select[id="year"]',
            'input[name="year"]',
        ], str(profile["birth_year"]))

        await human_sleep(1, 2)
        if not await submit_signup(page):
            raise RuntimeError("Unable to submit Spotify signup form")

        await human_sleep(7, 10)
        if await detect_captcha(page):
            raise RuntimeError("Captcha detected during Spotify signup")

        return {"fingerprint": fingerprint, "profile": profile}
    except Exception as exc:
        log_error(f"Signup failed for proxy {proxy['raw']}: {exc}")
        return None
    finally:
        if browser and playwright:
            await close_browser(playwright, browser)


async def create_accounts(count: int) -> None:
    ensure_directories()
    proxies = load_proxies()
    accounts = load_accounts() or []
    proxy_usage: dict[str, list[float]] = {}

    for _ in range(count):
        proxy = random.choice(proxies)
        usage = proxy_usage.setdefault(proxy["raw"], [])
        now = datetime.now(timezone.utc).timestamp()
        usage[:] = [timestamp for timestamp in usage if now - timestamp < 3600]
        if len(usage) >= 3:
            log_account_event(f"Skipping proxy {proxy['raw']} because it reached hourly limit")
            continue

        profile = build_profile()
        try:
            email, password, temp_token = await create_temp_email()
        except Exception as exc:
            log_error(f"Failed to create temporary email: {exc}")
            continue

        profile["email"] = email
        profile["password"] = password
        profile["display_name"] = profile["username"]
        profile["proxy"] = proxy["raw"]

        signup_result = await create_account(proxy, profile)
        if not signup_result:
            usage.append(now)
            continue

        try:
            verification_link = await get_verification_link(temp_token)
        except Exception as exc:
            log_error(f"Verification email did not arrive for {email}: {exc}")
            usage.append(now)
            continue

        verify_playwright = None
        verify_browser = None
        try:
            verify_playwright, verify_browser, verify_context = await create_stealth_browser(proxy, signup_result["fingerprint"])
            verify_page = await verify_context.new_page()
            await verify_page.goto(verification_link, timeout=60000, wait_until="networkidle")
            await human_sleep(5, 7)
            if await detect_captcha(verify_page):
                raise RuntimeError("Captcha detected during verification navigation")
        except Exception as exc:
            log_error(f"Verification navigation failed for {email}: {exc}")
            usage.append(now)
            continue
        finally:
            if verify_browser and verify_playwright:
                await close_browser(verify_playwright, verify_browser)

        account_record = {
            "email": email,
            "password": password,
            "username": profile["display_name"],
            "birthdate": f"{profile['birth_year']}-{profile['birth_month']:02d}-{profile['birth_day']:02d}",
            "proxy": proxy["raw"],
            "temp_mail_token": temp_token,
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "cookie_file": None,
            "fingerprint": signup_result["fingerprint"],
        }
        accounts.append(account_record)
        save_accounts(accounts)
        log_account_event(f"Created Spotify account {email} using proxy {proxy['raw']}")
        usage.append(now)


def main() -> None:
    parser = argparse.ArgumentParser(description="Spotify free account generator")
    parser.add_argument("--count", type=int, default=1, help="Number of accounts to create")
    args = parser.parse_args()
    asyncio.run(create_accounts(args.count))


if __name__ == "__main__":
    main()
