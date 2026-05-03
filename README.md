┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         FASE 0 - BIKIN LAGU GRATIS                                        │
│                             (Hari 1)                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  1. BIKIN LAGU PAKE SUNO AI (FREE TIER)                                                   │
│     • Buka suno.com → Free account (50 credits/day)                                       │
│     • Prompt: "lofi hip hop beats, instrumental, 2 minutes"                               │
│     • Download .mp3                                                                       │
│     • Audio enhance: Adobe Podcast Enhance (gratis)                                       │
│     • Simpan: my_track.mp3                                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  2. BIKIN COVER ART (CANVA FREE)                                                          │
│     • Canva.com → Template "Album Cover Minimalist"                                       │
│     • Teks judul lagu + nama artis                                                        │
│     • Download 3000x3000 PNG                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  3. UPLOAD KE DISTRIBUTOR GRATIS (ROUTENOTE)                                              │
│     • Routenote Free: 85% revenue buat lo, 15% buat Routenote                             │
│     • Hanya centang SPOTIFY                                                               │
│     • Release date: 2 minggu dari sekarang                                                │
│     • ⏳ Tunggu 5-10 hari kerja approval                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         FASE 1 - PERSIAPAN INFRASTRUKTUR BOT                            │
│                             (Hari 1-7)                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  4. BELI PROXY RESIDENTIAL (WAJIB - MODAL SATU-SATUNYA)                                   │
│     • Spotify free account SANGAT ketat soal IP.                                          │
│     • 1 IP publik cuma bisa 1-2 akun free sebelum kena CAPTCHA.                           │
│     • LO BUTUH: Proxy Residential Rotating.                                               │
│     • Rekomendasi murah:                                                                  │
│       - Webshare.io Residential Proxy: $7/bulan untuk 100 IP                              │
│       - IPRoyal Residential: $7/bulan untuk 1GB traffic                                   │
│       - Bright Data (mahal tapi paling bersih)                                            │
│     • ATAU alternatif gratisan: PAKAI VPN GRATIS TAPI GANTI-GANTI SERVER (ribet).         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  5. SETUP VPS (TEMPAT BOT JALAN 24 JAM)                                                   │
│     • VPS Murah: Contabo VPS S (Rp 120k/bulan) ATAU...                                    │
│     • GRATIS: Oracle Cloud Free Tier (4 ARM core, 24GB RAM!)                              │
│       - Daftar di oracle.com/cloud/free                                                   │
│       - Perlu kartu kredit buat verifikasi (gak di-charge)                                │
│       - Dapet VPS permanen gratis                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FASE 2 - OTOMATISASI PEMBUATAN AKUN SPOTIFY                            │
│                         (Script Python + Temp Mail)                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  6. SCRIPT AUTO-REGISTER SPOTIFY FREE                                                     │
│                                                                                          │
│  Algoritma per akun:                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: Generate data fake                                                        │   │
│  │          • Nama: Random dari Faker library (nama barat)                            │   │
│  │          • Username: random_string_12char                                         │   │
│  │          • Password: random complex password                                      │   │
│  │          • Birthdate: 1990-2000 (harus >18 tahun)                                 │   │
│  │                                                                                   │   │
│  │  STEP 2: Bikin email temporary                                                     │   │
│  │          • API: mail.tm atau guerrillamail.com                                    │   │
│  │          • Atau: mail.gw (API gampang)                                            │   │
│  │          • Dapetin: email@domain + token                                          │   │
│  │                                                                                   │   │
│  │  STEP 3: Register Spotify                                                          │   │
│  │          • POST ke https://www.spotify.com/api/signup                              │   │
│  │          • Headers: User-Agent random, Proxy Residential                          │   │
│  │          • Body: {email, password, username, birthdate, gender}                   │   │
│  │                                                                                   │   │
│  │  STEP 4: Verifikasi email                                                          │   │
│  │          • GET inbox dari temp mail API                                            │   │
│  │          • Cari email dari "spotify@spotify.com"                                   │   │
│  │          • Extract link verifikasi                                                │   │
│  │          • GET link tersebut → Akun AKTIF                                         │   │
│  │                                                                                   │   │
│  │  STEP 5: Simpan credentials                                                       │   │
│  │          • Simpan ke accounts.json: {email, password, username, proxy_ip}          │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  7. OTOMATISASI LOGIN + PLAYBACK (INI CORE BOTNYA)                                        │
│                                                                                          │
│  Karena ini FREE ACCOUNT (bukan premium), lo gak bisa pake librespot/spotifyd.            │
│  HARUS PAKE BROWSER AUTOMATION.                                                          │
│                                                                                          │
│  Tools:                                                                                  │
│  • Playwright (Python) - lebih stealth dari Selenium                                     │
│  • playwright-stealth - bypass bot detection                                             │
│                                                                                          │
│  Algoritma per bot instance:                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │  STEP 1: Launch browser (Chromium headless)                                       │   │
│  │          • Proxy: Residential proxy dari list                                     │   │
│  │          • User-Agent: Random modern Chrome                                       │   │
│  │          • Viewport: Random (1366x768, 1920x1080, etc)                            │   │
│  │          • Geolocation: Spoof ke negara Tier 1 (US/UK)                            │   │
│  │          • Timezone: Sesuai geolocation                                           │   │
│  │          • WebGL: Spoof fingerprint                                               │   │
│  │                                                                                   │   │
│  │  STEP 2: Buka open.spotify.com                                                    │   │
│  │          • Klik "Log In"                                                          │   │
│  │          • Isi email + password                                                   │   │
│  │          • Jeda random 2-5 detik antar ketikan (human-like)                       │   │
│  │          • Klik "Log In"                                                          │   │
│  │                                                                                   │   │
│  │  STEP 3: Handle popup/hambatan                                                    │   │
│  │          • Jika muncul CAPTCHA: Pause bot, log error, skip akun ini              │   │
│  │          • Jika muncul "Verify your email": Akun belum verified, skip            │   │
│  │          • Jika muncul "Premium popup": Klik "Skip" / "Not now"                   │   │
│  │          • Jika muncul "Cookie consent": Klik "Accept all"                        │   │
│  │                                                                                   │   │
│  │  STEP 4: Navigasi ke playlist lo                                                  │   │
│  │          • Buka URL: open.spotify.com/playlist/{PLAYLIST_ID}                       │   │
│  │          • Tunggu load 5 detik                                                    │   │
│  │          • Klik tombol "Play" (selector: button[aria-label="Play"])               │   │
│  │                                                                                   │   │
│  │  STEP 5: Enable loop + maintain playback                                          │   │
│  │          • Klik "Loop" button (selector: button[aria-label*="loop"])              │   │
│  │          • Set volume ke 100% (stream count track)                                │   │
│  │          • TAPI browser dimute di level OS (tetep keitung stream)                  │   │
│  │                                                                                   │   │
│  │  STEP 6: Monitoring loop                                                          │   │
│  │          • Tiap 60 detik: cek apakah masih playing                                │   │
│  │          • Ada 3 kondisi:                                                         │   │
│  │            1. Masih playing → lanjut                                              │   │
│  │            2. Pause karena iklan FREE → tunggu 30 detik → klik "Play" lagi       │   │
│  │            3. Error/Crash → restart browser → login ulang                         │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FASE 3 - STRATEGI BYPASS SPOTIFY FREE                               │
│                    (Ini yang bikin susah free account)                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  TANTANGAN SPOTIFY FREE ACCOUNT:                                                        │
│                                                                                         │
│  1. IKLAN TIAP 2-3 LAGU                                                                 │
│     • Free account DIPAKSA dengerin iklan 30 detik.                                     │
│     • Bot harus detect iklan → tunggu → klik "Skip Ad" kalau ada.                       │
│     • Kalau gak di-skip, playback BERHENTI total.                                       │
│                                                                                         │
│  2. CAPTCHA SAAT LOGIN                                                                  │
│     • Spotify pake reCAPTCHA v3 (invisible) + FunCaptcha (Arkose Labs).                 │
│     • Solusi:                                                                           │
│       - Pakai proxy RESIDENTIAL (bukan datacenter).                                     │
│       - Jangan login >5 akun per IP.                                                    │
│       - Gunakan cookies persistence (simpan cookies, reuse).                            │
│       - Kalau kena FunCaptcha: butuh jasa solving (2captcha / capsolver).               │
│                                                                                         │
│  3. RATE LIMIT API                                                                      │
│     • Spotify Web API rate limit: 180 request/menit per app.                            │
│     • Playback API (play/pause): lebih ketat.                                           │
│     • Solusi: Jangan pake API, pake browser automation (Playwright).                    │
│                                                                                         │
│  4. STREAM COUNT FREE vs PREMIUM                                                        │
│     • Free account stream = RPM lebih rendah.                                           │
│     • Estimasi: $0.50 - $1 per 1000 stream (vs $3-4 premium).                           │
│                                                                                         │
│  5. AKUN FREE MUDAH KENA BAN                                                            │
│     • Spotify detect "suspicious activity" → forced password reset.                     │
│     • Kalau banyak akun kena ban dari IP sama → IP di-blacklist.                        
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  SOLUSI BYPASS:                                                                         │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  1. COOKIE PERSISTENCE                                                          │    │
│  │     • Setelah login pertama, SIMPAN cookies (Playwright storage_state).         │    │
│  │     • Reuse cookies untuk sesi berikutnya → hindari login ulang.                │    │ 
│  │     • Cookies valid ~1-2 minggu.                                                │    │
│  │                                                                                 │    │
│  │  2. HUMAN BEHAVIOR SIMULATION                                                   │    │
│  │     • Random mouse movement sebelum klik.                                       │    │
│  │     • Scroll playlist pelan-pelan sebelum play.                                 │    │
│  │     • Jeda random 30-120 detik antar aksi.                                      │    │
│  │     • Kadang like lagu, kadang tidak (random).                                  │    │
│  │                                                                                 │    │
│  │  3. ROTASI IP PER AKUN                                                          │    │
│  │     • 1 akun = 1 IP residential tetap (jangan ganti-ganti).                     │    │
│  │     • Gunakan proxy sticky session.                                             │    │
│  │                                                                                 │    │
│  │  4. CAPTCHA SOLVING (JIKA TERJADI)                                              │    │ 
│  │     • Integrasi dengan Capsolver.com (bayar per solve ~$0.5/1000 captcha).      │    │
│  │     • Atau: skip akun yang kena captcha, bikin akun baru.                       │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FASE 4 - ARSITEKTUR BOT FULL SYSTEM                                 │
│                     (Struktur File Final)                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  spotify-bot-free/                                                                      │
│  ├── config/                                                                            │
│  │   ├── accounts.json          # [{email, password, proxy, cookies_file}]              │
│  │   ├── playlist.json          # {playlist_id, track_uris}                             │
│  │   └── proxies.txt            # List proxy residential                                │
│  │                                                                                      │
│  ├── data/                                                                              │
│  │   └── cookies/               # Playwright cookies per akun                           │
│  │       ├── acc_01_cookies.json                                                        │
│  │       ├── acc_02_cookies.json                                                        │
│  │       └── ...                                                                        │
│  │                                                                                      │
│  ├── logs/                                                                              │
│  │   ├── streams.log                                                                    │
│  │   └── errors.log                                                                     │
│  │                                                                                      │
│  ├── scripts/                                                                           │
│  │   ├── account_generator.py   # Auto-register Spotify free pake temp mail             │
│  │   ├── session_creator.py     # Login & simpan cookies per akun                       │
│  │   └── playlist_setup.py      # Bikin playlist 1:3 ratio                              │
│  │                                                                                      │
│  ├── src/                                                                               │
│  │   ├── main.py                # Orchestrator (spawn X browser instances)              │
│  │   ├── browser_pool.py        # Manage browser instances & proxy assignment           │
│  │   ├── bot_worker.py          # Individual bot logic (login, play, monitor)           │
│  │   ├── human_emulator.py      # Random delays, clicks, scrolls                        │
│  │   ├── captcha_handler.py     # Deteksi & solve captcha (optional Capsolver)          │
│  │   ├── ad_detector.py         # Deteksi iklan audio & skip                            │
│  │   └── health_monitor.py      # Cek status semua bot, restart jika mati               │
│  │                                                                                      │
│  ├── requirements.txt                                                                   │
│  ├── install.sh                                                                         │
│  └── README.md                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
