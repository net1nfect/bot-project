"""Konfigurasi global untuk eksperimen analisis pertahanan platform streaming.
Semua nilai di sini adalah parameter yang akan diuji dalam penelitian."""
from pathlib import Path
from .selectors import SELECTORS

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
SESSION_DIR = DATA_DIR / "sessions"
FINGERPRINT_DIR = DATA_DIR / "fingerprints"

# === Eksperimen Parameters ===
MAX_CONCURRENT_WORKERS = 5       # Jumlah worker bersamaan (uji threshold)
BROWSER_HEADLESS = True          # Mode tanpa GUI untuk efisiensi
LOGIN_TIMEOUT_SECONDS = 30       # Timeout halaman login
PLAYLIST_LOAD_TIMEOUT = 15       # Timeout muat playlist
HEALTH_CHECK_INTERVAL = 30       # Interval pengecekan kesehatan worker
RESTART_DELAY_SECONDS = 30       # Jeda sebelum restart worker gagal

# === Playlist Target (KONTEN MILIK PENELITI) ===
TARGET_PLAYLIST_URL = "https://open.spotify.com/playlist/XXXXXXXXX"

# === Daftar Proxy yang digunakan dalam eksperimen ===
PROXY_ADDRESSES = [
    # Contoh proxy format http://user:pass@host:port atau host:port
]

# === Daftar User-Agent untuk Rotasi ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]

# === Daftar Viewport untuk Rotasi ===
VIEWPORTS = [
    {"width": 1366, "height": 768},
    {"width": 1920, "height": 1080},
    {"width": 1440, "height": 900},
    {"width": 1536, "height": 864},
]

# === Selector CSS (hasil pemetaan UI) ===
SELECTORS = SELECTORS
