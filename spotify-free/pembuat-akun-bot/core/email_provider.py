"""Integrasi email sementara dengan layanan mail.gw untuk verifikasi registrasi.

Modul ini membuat akun email sementara, mem-poll inbox untuk pesan verifikasi,
dan menghapus akun ketika eksperimen selesai.
"""

from __future__ import annotations

import asyncio
import re
import secrets
from typing import Any, Dict, Optional, Tuple

import httpx

MAIL_GW_BASE_URL = "https://api.mail.gw"
VERIFICATION_SENDER_PATTERN = re.compile(r"spotify", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://[\w\-./?=&#%]+")


def _random_localpart() -> str:
    return f"lab{secrets.token_hex(6)}"


def _random_password(length: int = 14) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


class MailGwProvider:
    """Abstraksi akses ke API mail.gw untuk akun email sementara."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=MAIL_GW_BASE_URL, timeout=30.0)

    async def create_account(self) -> Tuple[str, str, str, str]:
        """Buat akun email sementara dan kembalikan alamat serta token akses."""
        local_part = _random_localpart()
        password = _random_password()
        address = f"{local_part}@mail.gw"

        payload = {"address": address, "password": password}
        response = await self._client.post("/accounts", json=payload)
        response.raise_for_status()
        data = response.json().get("data", {})
        account_id = data.get("id")
        if not account_id:
            raise RuntimeError("Gagal membuat akun mail.gw")

        token = await self._create_token(address, password)
        return address, token, account_id, password

    async def _create_token(self, address: str, password: str) -> str:
        payload = {"address": address, "password": password}
        response = await self._client.post("/token", json=payload)
        response.raise_for_status()
        token_data = response.json().get("data", {})
        token = token_data.get("token")
        if not token:
            raise RuntimeError("Gagal mendapatkan token mail.gw")
        return token

    async def get_verification_link(self, email_token: str, timeout: int = 120) -> str:
        """Polling inbox hingga menemukan link verifikasi dari pengirim Spotify."""
        headers = {"Authorization": f"Bearer {email_token}"}
        deadline = asyncio.get_event_loop().time() + timeout

        while asyncio.get_event_loop().time() < deadline:
            response = await self._client.get("/messages", headers=headers, params={"page": 1, "limit": 20})
            response.raise_for_status()
            messages = response.json().get("hydra:member", [])

            for message in messages:
                if VERIFICATION_SENDER_PATTERN.search(str(message.get("from"))):
                    message_id = message.get("id")
                    if not message_id:
                        continue
                    body = await self._fetch_message_body(message_id, headers)
                    link = self._extract_verification_link(body)
                    if link:
                        return link

            await asyncio.sleep(5)

        raise TimeoutError("Timeout menunggu email verifikasi dari mail.gw")

    async def _fetch_message_body(self, message_id: str, headers: Dict[str, str]) -> str:
        response = await self._client.get(f"/messages/{message_id}", headers=headers)
        response.raise_for_status()
        data = response.json().get("data", {})
        html = data.get("html") or ""
        text = data.get("text") or ""
        return html if html else text

    def _extract_verification_link(self, body: str) -> Optional[str]:
        if not body:
            return None
        match = URL_PATTERN.search(body)
        return match.group(0) if match else None

    async def delete_account(self, email_token: str, account_id: str) -> None:
        """Hapus akun sementara dari mail.gw untuk membersihkan sumber daya."""
        headers = {"Authorization": f"Bearer {email_token}"}
        try:
            response = await self._client.delete(f"/accounts/{account_id}", headers=headers)
            if response.status_code not in {200, 204}:
                raise httpx.HTTPStatusError("Delete account failed", request=response.request, response=response)
        except Exception:
            pass

    async def close(self) -> None:
        await self._client.aclose()
