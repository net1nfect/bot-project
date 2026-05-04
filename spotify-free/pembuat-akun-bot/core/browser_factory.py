"""Pabrikasi browser Chromium stealth untuk eksperimen fingerprinting dan registrasi."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from config import settings


@dataclass
class BrowserSession:
    browser: Browser
    context: BrowserContext
    page: Page
    user_agent: str
    viewport: Dict[str, int]


def _random_choice(collection: list[Any]) -> Any:
    return random.choice(collection)


def _build_fingerprint_script() -> str:
    return r"""
(function () {
    Object.defineProperty(navigator, 'webdriver', {get: () => false});
    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});

    const makeNoise = (canvas) => {
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            return;
        }
        const shift = { 'r': Math.floor(Math.random() * 10), 'g': Math.floor(Math.random() * 10), 'b': Math.floor(Math.random() * 10) };
        const width = canvas.width;
        const height = canvas.height;
        const imageData = ctx.getImageData(0, 0, width, height);
        for (let i = 0; i < imageData.data.length; i += 4) {
            imageData.data[i] = imageData.data[i] + shift.r;
            imageData.data[i + 1] = imageData.data[i + 1] + shift.g;
            imageData.data[i + 2] = imageData.data[i + 2] + shift.b;
        }
        ctx.putImageData(imageData, 0, 0);
    };

    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function () {
        makeNoise(this);
        return originalToDataURL.apply(this, arguments);
    };

    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function () {
        const context = originalGetContext.apply(this, arguments);
        if (arguments[0] === 'webgl' || arguments[0] === 'experimental-webgl') {
            const originalGetParameter = context.getParameter.bind(context);
            context.getParameter = function (parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return originalGetParameter(parameter);
            };
        }
        return context;
    };
})();
"""


async def create_browser_session(
    proxy: Optional[str] = None,
    timezone: Optional[str] = "UTC",
    geolocation: Optional[Dict[str, float]] = None,
    storage_state: Optional[Path] = None,
    headless: bool = True,
) -> BrowserSession:
    """Menciptakan sesi browser yang dikonfigurasi untuk menghindari deteksi otomatisasi."""
    user_agent = _random_choice(settings.USER_AGENTS)
    viewport = _random_choice(settings.VIEWPORTS)
    browser_args = ["--disable-blink-features=AutomationControlled", "--no-sandbox"]

    playwright = await async_playwright().start()
    launch_kwargs: Dict[str, Any] = {
        "headless": headless,
        "args": browser_args,
    }
    if proxy:
        launch_kwargs["proxy"] = {"server": proxy}

    browser = await playwright.chromium.launch(**launch_kwargs)

    context_kwargs: Dict[str, Any] = {
        "user_agent": user_agent,
        "viewport": viewport,
        "locale": "en-US",
        "timezone_id": timezone or "UTC",
        "ignore_https_errors": True,
        "permissions": ["geolocation"],
    }
    if storage_state:
        context_kwargs["storage_state"] = str(storage_state)
    if geolocation:
        context_kwargs["geolocation"] = geolocation

    context = await browser.new_context(**context_kwargs)
    await context.add_init_script(_build_fingerprint_script())
    page = await context.new_page()

    return BrowserSession(browser=browser, context=context, page=page, user_agent=user_agent, viewport=viewport)
