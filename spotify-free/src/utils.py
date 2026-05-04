import json
import logging
import random
import re
import string
from datetime import datetime, timezone
from pathlib import Path

from faker import Faker
from config.settings import (
    ACCOUNTS_FILE,
    COOKIES_DIR,
    DATA_DIR,
    FINGERPRINTS_FILE,
    LOG_DIR,
    PLAYLIST_CONFIG,
    PROXY_FILE,
    STREAMS_LOG,
    ACCOUNTS_LOG,
    ERRORS_LOG,
    DEFAULT_USER_AGENT,
    DEFAULT_VIEWPORT,
    DEFAULT_TIMEZONE,
    DEFAULT_LOCALE,
    DEFAULT_GEOLOCATION,
)

faker = Faker()
Faker.seed_instance(12345)

USER_AGENTS = [
    DEFAULT_USER_AGENT,
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

VIEWPORTS = [
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1536, "height": 864},
    {"width": 1920, "height": 1080},
]

TIMEZONES = [
    "America/New_York",
    "Europe/London",
    "America/Los_Angeles",
    "Europe/Berlin",
    "America/Chicago",
]

GEOLOCATIONS = [
    {"latitude": 40.7128, "longitude": -74.0060},
    {"latitude": 51.5074, "longitude": -0.1278},
    {"latitude": 34.0522, "longitude": -118.2437},
    {"latitude": 48.1351, "longitude": 11.5820},
]


def ensure_directories() -> None:
    """Create all runtime directories so scripts can write safely."""
    for path in [DATA_DIR, LOG_DIR, COOKIES_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default=None):
    """Load a JSON file with fallback if missing or invalid."""
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: Path, payload) -> None:
    """Save structured data reliably with indentation for readability."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def append_log(path: Path, message: str) -> None:
    """Append a timestamped line to a log file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    path.open("a", encoding="utf-8").write(f"{timestamp} | {message}\n")


def parse_proxy_line(line: str) -> dict | None:
    """Parse a proxy line in host:port:user:pass format."""
    cleaned = line.strip()
    if not cleaned or cleaned.startswith("#"):
        return None
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        cleaned = cleaned.split("://", 1)[1]
    parts = cleaned.split(":")
    if len(parts) != 4:
        return None
    host, port, username, password = parts
    server = f"http://{host}:{port}"
    return {
        "server": server,
        "username": username,
        "password": password,
        "raw": cleaned,
    }


def random_password(length: int = 16) -> str:
    """Generate a strong password suitable for Spotify registration."""
    if length < 12:
        length = 12
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    return "".join(random.choice(alphabet) for _ in range(length))


def random_username() -> str:
    """Generate a plausible username for Spotify sign-up."""
    base = faker.user_name().lower()
    suffix = random.randint(100, 9999)
    return re.sub(r"[^a-z0-9_]", "", f"{base}_{suffix}")[:20]


def build_profile() -> dict:
    """Build a fake identity profile for account creation."""
    birth_year = random.randint(1990, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    first_name = faker.first_name()
    last_name = faker.last_name()
    username = random_username()
    password = random_password()
    return {
        "first_name": first_name,
        "last_name": last_name,
        "display_name": username,
        "username": username,
        "password": password,
        "birth_day": birth_day,
        "birth_month": birth_month,
        "birth_year": birth_year,
        "gender": random.choice(["male", "female", "non-binary"]),
    }


def generate_fingerprint(account_email: str | None = None) -> dict:
    """Create a realistic browser fingerprint for Playwright contexts."""
    return {
        "account": account_email,
        "user_agent": random.choice(USER_AGENTS),
        "viewport": random.choice(VIEWPORTS),
        "timezone": random.choice(TIMEZONES),
        "locale": DEFAULT_LOCALE,
        "geolocation": random.choice(GEOLOCATIONS),
        "canvas_hash": "%032x" % random.getrandbits(128),
    }


def load_accounts() -> list[dict]:
    """Load account records from the shared JSON store."""
    accounts = load_json(ACCOUNTS_FILE, default=[])
    return accounts if isinstance(accounts, list) else []


def save_accounts(accounts: list[dict]) -> None:
    """Persist account records to disk."""
    save_json(ACCOUNTS_FILE, accounts)


def load_fingerprints() -> list[dict]:
    """Load fingerprint metadata for accounts."""
    fingerprints = load_json(FINGERPRINTS_FILE, default=[])
    return fingerprints if isinstance(fingerprints, list) else []


def save_fingerprints(items: list[dict]) -> None:
    """Save fingerprint metadata to disk."""
    save_json(FINGERPRINTS_FILE, items)


def get_account_cookie_path(account: dict, index: int) -> Path:
    """Derive a deterministic cookie storage path for an account."""
    sanitized = re.sub(r"[^a-zA-Z0-9_.@-]", "_", account.get("email", f"account_{index}"))
    return COOKIES_DIR / f"{sanitized}_cookies.json"


def get_playlist_config() -> dict:
    """Load playlist metadata from config file."""
    return load_json(PLAYLIST_CONFIG, default={}) or {}


def make_logger(name: str, log_file: Path) -> logging.Logger:
    """Create a logger writing to both console and a log file."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def log_error(message: str) -> None:
    append_log(ERRORS_LOG, message)


def log_account_event(message: str) -> None:
    append_log(ACCOUNTS_LOG, message)


def log_stream_event(message: str) -> None:
    append_log(STREAMS_LOG, message)
