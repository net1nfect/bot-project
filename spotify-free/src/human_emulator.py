import random
import asyncio
from typing import Optional
from playwright.async_api import Page, ElementHandle

from config.settings import HUMAN_MOVE_INTERVAL, HUMAN_MOVE_INTERVAL_MAX


def random_delay(min_sec: float = 0.5, max_sec: float = 2.0) -> float:
    """Choose a randomized pause interval to simulate human thinking."""
    delay = random.uniform(min_sec, max_sec)
    return delay


async def human_sleep(min_sec: float = 0.5, max_sec: float = 2.0) -> None:
    """Sleep for a randomized duration."""
    await asyncio.sleep(random_delay(min_sec, max_sec))


async def human_type(page: Page, selector: str, text: str, min_delay: int = 50, max_delay: int = 200) -> None:
    """Type text with per-character delays and occasional human-like corrections."""
    await page.focus(selector)
    for char in text:
        await page.keyboard.type(char)
        await asyncio.sleep(random.uniform(min_delay / 1000.0, max_delay / 1000.0))
        if random.random() < 0.03:
            await page.keyboard.press("Backspace")
            await asyncio.sleep(random.uniform(0.05, 0.15))
            await page.keyboard.type(char)
    await asyncio.sleep(random.uniform(0.1, 0.4))


async def human_click(page: Page, selector: str) -> None:
    """Move the mouse toward the element and click it with a small delay."""
    element = await page.query_selector(selector)
    if not element:
        raise ValueError(f"Unable to find element for human_click: {selector}")
    box = await element.bounding_box()
    if not box:
        await element.click()
        return
    start_x = random.randint(100, 300)
    start_y = random.randint(100, 300)
    await page.mouse.move(start_x, start_y, steps=10)
    await asyncio.sleep(random.random() * 0.2)
    target_x = box["x"] + box["width"] / 2 + random.uniform(-5, 5)
    target_y = box["y"] + box["height"] / 2 + random.uniform(-5, 5)
    await page.mouse.move(target_x, target_y, steps=12)
    await asyncio.sleep(random.uniform(0.1, 0.25))
    await page.mouse.click(target_x, target_y)
    await asyncio.sleep(random.uniform(0.25, 0.6))


async def random_scroll(page: Page, min_pixels: int = 200, max_pixels: int = 450) -> None:
    """Scroll slowly in a random direction to appear human-like."""
    distance = random.randint(min_pixels, max_pixels)
    direction = random.choice([1, -1])
    await page.mouse.wheel(0, distance * direction)
    await asyncio.sleep(random.uniform(0.5, 1.5))


async def random_micro_movement(page: Page) -> None:
    """Perform tiny mouse jitter movements every few seconds."""
    while True:
        await asyncio.sleep(random.uniform(HUMAN_MOVE_INTERVAL, HUMAN_MOVE_INTERVAL_MAX))
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        await page.mouse.move(x, y, steps=5)
        await asyncio.sleep(0.2)


async def click_if_visible(page: Page, selector: str) -> bool:
    """Click the element when visible; otherwise return False."""
    element = await page.query_selector(selector)
    if element and await element.is_visible():
        await human_click(page, selector)
        return True
    return False
