# spotify bot free

project ini dibuat buat ngejalanin spotify free account streaming secara otomatis di linux tanpa gui.

## apa yang kerjain sistem ini

- bikin akun spotify free pake temp mail otomatis.
- login ke spotify lewat browser headless pake playwright.
- simpan cookie session supaya bot gak login ulang terus.
- puter playlist target terus-menerus dengan deteksi iklan.
- pakai proxy residensial biar session lebih stabil.

## struktur file

```
spotify-bot-free/
├── config/
│   ├── settings.py
│   ├── proxies.txt
│   └── playlist.json
├── data/
│   ├── accounts.json
│   ├── fingerprints.json
│   └── cookies/
├── logs/
│   ├── streams.log
│   ├── accounts.log
│   └── errors.log
├── scripts/
│   ├── account_generator.py
│   ├── session_initializer.py
│   └── playlist_setup.py
├── src/
│   ├── main.py
│   ├── bot_instance.py
│   ├── browser_utils.py
│   ├── human_emulator.py
│   ├── ad_handler.py
│   ├── captcha_solver.py
│   ├── temp_mail.py
│   └── utils.py
├── requirements.txt
├── install.sh
└── README.md
```

## cara pakai

1. masuk ke folder proyek:
   ```bash
   cd /bot-project/spotify-free
   ```
2. isi proxy residensial di `config/proxies.txt` dengan format:
   ```text
   host:port:username:password
   ```
3. isi `config/playlist.json` dengan playlist spotify target kamu.
4. jalankan install script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
5. setelah install selesai, aktifkan lingkungan python jika belum diaktifkan:
   ```bash
   source venv/bin/activate
   ```
6. buat akun spotify free otomatis:
   ```bash
   python scripts/account_generator.py --count 5
   ```
7. login sekali dan simpan cookie:
   ```bash
   python scripts/session_initializer.py
   ```
8. jalankan bot utama:
   ```bash
   python src/main.py
   ```
9. cek log realtime:
   ```bash
   tail -f logs/streams.log logs/errors.log
   ```

## catatan penting

- gunakan proxy residensial, jangan pake proxy datacenter murah.
- buat akun baru di proxy beda-beda, maksimal 3 akun per ip per jam.
- simpan cookie supaya bot bisa lanjut tanpa login ulang.
- playlist harus campur lagu kamu dengan lagu ambient/popular, jangan 100% doa sendiri.
- kalau ada error, cek `logs/errors.log` dan `logs/accounts.log`.

## penjelasan singkat tiap file

- `config/settings.py`: konfigurasi path, selector spotify, timing, dan parameter bot.
- `config/proxies.txt`: daftar proxy residensial untuk tiap akun.
- `config/playlist.json`: playlist spotify target yang akan diputar.
- `data/accounts.json`: daftar akun spotify yang dibuat.
- `data/fingerprints.json`: data fingerprint browser untuk tiap akun.
- `data/cookies/`: cookie/session state dari tiap akun.
- `logs/streams.log`: event streaming dan status bot.
- `logs/accounts.log`: catatan pembuatan akun dan inisialisasi.
- `logs/errors.log`: error dan crash bot.
- `scripts/account_generator.py`: bikin akun spotify free otomatis.
- `scripts/session_initializer.py`: login sekali dan simpan cookie.
- `scripts/playlist_setup.py`: helper simpan playlist id.
- `src/main.py`: jalankan semua bot akun secara paralel.
- `src/bot_instance.py`: logika main bot per akun untuk play, loop, dan monitoring.
- `src/browser_utils.py`: setup browser playwright stealth dan proxy.
- `src/human_emulator.py`: simulasi perilaku manusia seperti ketik dan scroll.
- `src/ad_handler.py`: deteksi iklan spotify free dan penanganannya.
- `src/captcha_solver.py`: kerangka optional buat solve captcha kalau mau pakai 2captcha.
- `src/temp_mail.py`: wrapper temp mail mail.gw untuk verifikasi email.
- `src/utils.py`: helper umum buat log, config, dan generate data.
