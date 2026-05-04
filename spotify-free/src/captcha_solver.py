import os
import time
from typing import Optional

import httpx

CAPTCHA_API_URL = "http://2captcha.com"


class CaptchaSolverError(Exception):
    pass


class CaptchaSolver:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("TWO_CAPTCHA_API_KEY")
        if not self.api_key:
            raise CaptchaSolverError("2Captcha API key is required for captcha solving")

    async def solve_recaptcha_v2(self, site_key: str, page_url: str, timeout: int = 120) -> str:
        """Submit a reCAPTCHA V2 request and poll for the result."""
        with httpx.Client(timeout=30.0) as client:
            create_resp = client.post(
                f"{CAPTCHA_API_URL}/in.php",
                data={
                    "key": self.api_key,
                    "method": "userrecaptcha",
                    "googlekey": site_key,
                    "pageurl": page_url,
                    "json": 1,
                },
            )
            create_resp.raise_for_status()
            create_data = create_resp.json()
            if create_data.get("status") != 1:
                raise CaptchaSolverError(f"Captcha request failed: {create_data}")
            request_id = create_data.get("request")

            deadline = time.time() + timeout
            while time.time() < deadline:
                poll_resp = client.get(
                    f"{CAPTCHA_API_URL}/res.php",
                    params={
                        "key": self.api_key,
                        "action": "get",
                        "id": request_id,
                        "json": 1,
                    },
                )
                poll_resp.raise_for_status()
                poll_data = poll_resp.json()
                if poll_data.get("status") == 1:
                    return poll_data.get("request")
                if poll_data.get("request") not in ("CAPCHA_NOT_READY", "CAPTCHA_NOT_READY"):
                    raise CaptchaSolverError(f"Captcha solving failed: {poll_data}")
                time.sleep(5)

        raise CaptchaSolverError("Captcha solve timed out")
