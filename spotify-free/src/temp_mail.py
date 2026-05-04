import asyncio
import random
import re
import string
from pathlib import Path
from typing import Optional

import httpx
from config.settings import TEMP_MAIL_API_BASE, TEMP_MAIL_HEADERS
from src.utils import append_log


def _random_local_part(length: int = 10) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


async def get_mailgw_domain() -> Optional[str]:
    async with httpx.AsyncClient(headers=TEMP_MAIL_HEADERS, timeout=30.0) as client:
        response = await client.get(f"{TEMP_MAIL_API_BASE}/domains")
        response.raise_for_status()
        payload = response.json()
        if not payload or "hydra:member" not in payload:
            return None
        domains = payload.get("hydra:member", [])
        if not domains:
            return None
        return domains[0].get("domain")


async def create_temp_email() -> tuple[str, str, str]:
    """Create a temporary email account and return email, password, token."""
    domain = await get_mailgw_domain()
    if not domain:
        raise RuntimeError("Unable to obtain temporary mail domain from mail.gw")

    local_part = _random_local_part(12)
    address = f"{local_part}@{domain}"
    password = _random_local_part(16)
    body = {"address": address, "password": password}

    async with httpx.AsyncClient(headers=TEMP_MAIL_HEADERS, timeout=30.0) as client:
        response = await client.post(f"{TEMP_MAIL_API_BASE}/accounts", json=body)
        if response.status_code not in (200, 201):
            raise RuntimeError(f"Failed to create temp mail account: {response.text}")

        login_response = await client.post(
            f"{TEMP_MAIL_API_BASE}/token",
            data={"username": address, "password": password},
            headers={"Accept": "application/json"},
            timeout=30.0,
        )
        login_response.raise_for_status()
        token_data = login_response.json().get("data", {})
        token = token_data.get("token")
        if not token:
            raise RuntimeError("Temporary mail service did not return auth token")

    append_log(
        Path("logs") / "accounts.log",
        f"Created temp mail {address} with token length {len(token)}",
    )
    return address, password, token


async def get_verification_link(email_token: str, timeout: int = 60) -> str:
    """Poll the temporary inbox until a Spotify verification link arrives."""
    headers = {**TEMP_MAIL_HEADERS, "Authorization": f"Bearer {email_token}"}
    deadline = asyncio.get_event_loop().time() + timeout
    message_url = None

    async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
        while asyncio.get_event_loop().time() < deadline:
            response = await client.get(f"{TEMP_MAIL_API_BASE}/messages?page=1")
            response.raise_for_status()
            payload = response.json()
            messages = payload.get("hydra:member", [])
            for message in messages:
                subject = message.get("subject", "") or ""
                if "spotify" in subject.lower() or "verify" in subject.lower():
                    message_url = message.get("@id") or message.get("id")
                    break
            if message_url:
                break
            await asyncio.sleep(3)

        if not message_url:
            raise TimeoutError("Verification email did not arrive in the temporary inbox")

        message_id = message_url.split("/")[-1]
        detail = await client.get(f"{TEMP_MAIL_API_BASE}/messages/{message_id}")
        detail.raise_for_status()
        body = detail.json().get("text", "") or detail.json().get("html", "") or ""
        match = re.search(r'https://[^\"]*spotify[^\"]*', body)
        if not match:
            raise RuntimeError("Spotify verification link could not be extracted from temp mail message")

    return match.group(0)
