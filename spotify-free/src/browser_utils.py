import asyncio
from pathlib import Path
from typing import Optional, Tuple

from playwright.async_api import async_playwright, Browser, BrowserContext, Playwright
from config.settings import DEFAULT_LOCALE, PLAYWRIGHT_LAUNCH_ARGS


async def add_stealth_scripts(context: BrowserContext) -> None:
    """Inject stealth overrides into every new page."""
    stealth_js = r"""
        (() => {
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) =>
                parameters.name === 'notifications'
                    ? Promise.resolve({state: Notification.permission})
                    : originalQuery(parameters);
        })();
    """
    await context.add_init_script(stealth_js)


async def create_stealth_browser(
    proxy_config: dict,
    fingerprint: dict,
    storage_state: Optional[str] = None,
):
    """Start Chromium with a residential proxy and fingerprint overrides."""
    playwright = await async_playwright().start()
    launch_args = list(PLAYWRIGHT_LAUNCH_ARGS)
    if proxy_config and proxy_config.get("server"):
        launch_args.append(f'--proxy-server={proxy_config["server"]}')

    browser: Browser = await playwright.chromium.launch(
        headless=True,
        args=launch_args,
    )

    context = await browser.new_context(
        proxy={
            "server": proxy_config.get("server"),
            "username": proxy_config.get("username"),
            "password": proxy_config.get("password"),
        }
        if proxy_config and proxy_config.get("server")
        else None,
        user_agent=fingerprint.get("user_agent"),
        viewport=fingerprint.get("viewport"),
        timezone_id=fingerprint.get("timezone"),
        geolocation=fingerprint.get("geolocation"),
        locale=DEFAULT_LOCALE,
        permissions=["notifications"],
        storage_state=storage_state,
        ignore_https_errors=True,
    )

    await add_stealth_scripts(context)
    return playwright, browser, context


async def close_browser(playwright: Playwright, browser: Browser) -> None:
    """Close browser safely, handling any internal cleanup exceptions."""
    try:
        await browser.close()
    except Exception:
        pass
    try:
        await playwright.stop()
    except Exception:
        pass
    try:
        await asyncio.sleep(0.5)
    except Exception:
        pass
