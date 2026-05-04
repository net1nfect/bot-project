from pathlib import Path

# Base directories for data, cookies, and logs.
# Keeping all storage under the project root simplifies deployment and backup.
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
COOKIES_DIR = DATA_DIR / "cookies"
PROXY_FILE = BASE_DIR / "config" / "proxies.txt"
PLAYLIST_CONFIG = BASE_DIR / "config" / "playlist.json"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"
FINGERPRINTS_FILE = DATA_DIR / "fingerprints.json"

# Limits for a Linux VPS with roughly 4GB RAM.
# Each Playwright browser instance can be heavy, so we keep concurrency low.
MAX_CONCURRENT_BOTS = 8
BROWSER_MEMORY_PER_INSTANCE_MB = 300
MAX_ACCOUNTS_PER_PROXY_PER_HOUR = 3
MAX_BOTS_PER_PROXY = 1

# Timing constants used throughout the system.
LOGIN_TIMEOUT = 30
PLAYLIST_LOAD_WAIT = 5
AD_CHECK_INTERVAL = 15
HEALTH_CHECK_INTERVAL = 60
RESTART_DELAY = 30
EMAIL_POLL_INTERVAL = 3
EMAIL_POLL_TIMEOUT = 60
HUMAN_TYPING_MIN_DELAY_MS = 50
HUMAN_TYPING_MAX_DELAY_MS = 200
HUMAN_MOVE_INTERVAL = 10
HUMAN_MOVE_INTERVAL_MAX = 30
TRACK_PLAYBACK_CHECK = 15
STREAM_LOG_INTERVAL = 60
AD_MAX_WAIT_SECONDS = 35
CAPTCHA_DETECTION_TIMEOUT = 15

# Default browser viewport and fingerprint templates.
DEFAULT_VIEWPORT = {"width": 1366, "height": 768}
DEFAULT_TIMEZONE = "America/New_York"
DEFAULT_LOCALE = "en-US"
DEFAULT_GEOLOCATION = {"latitude": 40.7128, "longitude": -74.0060}

# Spotify UI selectors for the 2024-2025 web interface.
# These selectors are intentionally broad enough to survive minor UI changes.
SELECTORS = {
    "signup_button": 'button[data-testid="register-button"]',
    "login_button": 'button[data-testid="login-button"], a[href*="login"]',
    "email_input": 'input[id="login-username"], input[name="email"]',
    "password_input": 'input[id="login-password"], input[type="password"]',
    "submit_login": 'button[id="login-button"], button[data-testid="login-button"]',
    "play_button": 'button[aria-label="Play"], button[data-testid="play-button"]',
    "pause_button": 'button[aria-label="Pause"], button[data-testid="pause-button"]',
    "loop_button": 'button[aria-label*="loop"], button[data-testid*="repeat"]',
    "cookie_accept": 'button[id="onetrust-accept-btn-handler"], button[data-testid="onetrust-cookie-policy"]',
    "premium_popup_close": 'button[aria-label="Close"], button[data-testid="close-button"]',
    "welcome_modal_close": 'button[aria-label="Close"], button[data-testid="close"]',
    "ad_playing": '[data-testid="ad-playing"], [data-testid*="ad"]',
    "skip_ad_button": 'button[data-testid="skip-ad-button"], button[aria-label*="Skip"]',
    "profile_menu": '[data-testid="user-widget-link"]',
    "login_form": 'form#login-form, form[action*="login"]',
}

# Supported temp mail provider and API settings.
TEMP_MAIL_API_BASE = "https://api.mail.gw"
TEMP_MAIL_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Logging settings.
STREAMS_LOG = LOG_DIR / "streams.log"
ACCOUNTS_LOG = LOG_DIR / "accounts.log"
ERRORS_LOG = LOG_DIR / "errors.log"

# Playback safety thresholds to mimic human streaming behavior.
MINIMUM_STREAM_SECONDS = 35
MAXIMUM_TRACK_SKIP_SECONDS = 45

# Playwright launch arguments for headless Linux VPS operation.
PLAYWRIGHT_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-gpu",
    "--disable-audio-output",
    "--disable-software-rasterizer",
    "--disable-setuid-sandbox",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-client-side-phishing-detection",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--metrics-recording-only",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--password-store=basic",
    "--use-mock-keychain",
]

# User-agent fallback if fingerprint does not provide one.
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
