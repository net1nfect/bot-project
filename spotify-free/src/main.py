import asyncio
from pathlib import Path

from config.settings import MAX_CONCURRENT_BOTS
from src.bot_instance import BotInstance
from src.utils import load_accounts, log_error, log_stream_event


def cookies_exist(account: dict) -> bool:
    cookie_path = account.get("cookie_file")
    return bool(cookie_path and Path(cookie_path).exists())


async def run_bot_with_semaphore(semaphore: asyncio.Semaphore, account: dict) -> None:
    async with semaphore:
        bot = BotInstance(account)
        await bot.run()


async def main() -> None:
    accounts = load_accounts()
    ready_accounts = [
        account for account in accounts if account.get("status") == "active" and cookies_exist(account)
    ]
    log_stream_event(f"Starting {len(ready_accounts)} bot instances")
    if not ready_accounts:
        raise RuntimeError("No ready Spotify accounts found. Make sure accounts.json and cookie files exist.")

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_BOTS)
    tasks = [asyncio.create_task(run_bot_with_semaphore(semaphore, account)) for account in ready_accounts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            log_error(f"Bot task failed: {result}")


if __name__ == "__main__":
    asyncio.run(main())
