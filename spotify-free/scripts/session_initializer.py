import argparse
import asyncio
from datetime import datetime, timezone
from pathlib import Path

from config.settings import SELECTORS
from src.browser_utils import close_browser, create_stealth_browser
from src.human_emulator import click_if_visible, human_sleep, human_type
from src.utils import (
    ensure_directories,
    get_account_cookie_path,
    generate_fingerprint,
    load_accounts,
    log_account_event,
    log_error,
    parse_proxy_line,
    save_accounts,
)

LOGIN_URL = "https://open.spotify.com/"


async def login_and_save(account: dict, index: int) -> None:
    if account.get("status") != "active":
        return
    proxy_config = parse_proxy_line(account.get("proxy", "")) or {}
    fingerprint = account.get("fingerprint") or generate_fingerprint(account.get("email"))
    cookie_path = get_account_cookie_path(account, index)
    playwright = None
    browser = None
    try:
        playwright, browser, context = await create_stealth_browser(proxy_config, fingerprint)
        page = await context.new_page()
        await page.goto(LOGIN_URL, timeout=60000, wait_until="load")
        await human_sleep(2, 4)
        await click_if_visible(page, SELECTORS.get("cookie_accept"))
        await human_sleep(1, 2)
        await click_if_visible(page, SELECTORS.get("login_button"))
        await human_sleep(2, 4)

        await human_type(page, SELECTORS.get("email_input"), account["email"])
        await human_sleep(0.5, 1.0)
        await human_type(page, SELECTORS.get("password_input"), account["password"])
        await human_sleep(1, 2)
        await click_if_visible(page, SELECTORS.get("submit_login"))
        await human_sleep(8, 12)

        await click_if_visible(page, SELECTORS.get("premium_popup_close"))
        await click_if_visible(page, SELECTORS.get("welcome_modal_close"))
        await human_sleep(3, 5)

        await context.storage_state(path=str(cookie_path))
        account["cookie_file"] = str(cookie_path)
        account["last_initialized_at"] = datetime.now(timezone.utc).isoformat()
        log_account_event(f"Saved storage state for {account['email']} to {cookie_path}")
    except Exception as exc:
        log_error(f"Session initialization failed for {account.get('email')}: {exc}")
    finally:
        if browser and playwright:
            await close_browser(playwright, browser)


async def initialize_sessions() -> None:
    ensure_directories()
    accounts = load_accounts()
    for index, account in enumerate(accounts, start=1):
        if account.get("status") != "active":
            continue
        cookie_file = account.get("cookie_file")
        if cookie_file and Path(cookie_file).exists():
            log_account_event(f"Skipping {account['email']} because cookie file already exists")
            continue
        await login_and_save(account, index)
        save_accounts(accounts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Spotify session initializer and cookie saver")
    args = parser.parse_args()
    asyncio.run(initialize_sessions())


if __name__ == "__main__":
    main()
