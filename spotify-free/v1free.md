# alur spotify free bot

ini adalah penjelasan alur lengkap buat sistem spotify free bot. semua ditulis pakai bahasa indonesia yang santai dan semua huruf kecil.

## fase 0 - bikin lagu gratis

1. bikin lagu pake suno.ai free tier.
2. gunakan prompt yang simple, misalnya: lo-fi hip hop beats instrumental 2 menit.
3. download file mp3.
4. kalau perlu, poles audio pake tool gratis seperti adobe podcast enhance.
5. simpan filenya jadi my_track.mp3.

## fase 1 - persiapan infrastruktur bot

1. sewa vps linux tanpa gui (ubuntu 22.04 recommended).
2. siapkan proxy residensial; ini wajib.
3. tiap akun spotify free harus jalan lewat ip berbeda atau sticky proxy.
4. simpan proxy di config/proxies.txt.
5. jangan paksakan banyak akun di satu ip dalam waktu singkat.

## fase 2 - bikin akun spotify free otomatis

1. jalankan `python scripts/account_generator.py --count 5`.
2. skrip ini akan:
   - bikin data fake pake faker.
   - buat email sementara lewat mail.gw.
   - open browser playwright headless.
   - daftar spotify pake proxy.
   - tunggu verifikasi email.
   - simpan akun di data/accounts.json.
3. setiap proxy hanya boleh dipake maksimal 3 akun per jam.
4. kalau muncul captcha saat signup, akun itu skip.

## fase 3 - login sekali dan simpan cookie

1. jalankan `python scripts/session_initializer.py`.
2. script ini akan login tiap akun satu kali.
3. setelah login berhasil, storage_state disimpan ke data/cookies/.
4. cookie ini penting supaya bot berikutnya gak perlu login ulang.

## fase 4 - jalankan bot utama

1. isi playlist target di config/playlist.json.
2. jalankan `python src/main.py`.
3. bot akan:
   - buka playlist pake browser headless.
   - klik play.
   - aktifkan loop.
   - mute audio di browser.
   - monitor status pemutaran.
   - deteksi iklan dan tunggu sampai selesai.
4. cek log di logs/streams.log dan logs/errors.log.

## cara gunakan file .md ini

- readme.md berisi tutorial langkah demi langkah.
- v1free.md berisi alur bot dan strategi singkat.
- baca dulu readme.md buat install dan setup.
- kalau butuh ide strategi bot, buka v1free.md.

## pesan penting

- bot ini buat spotify free, jadi harus tahan iklan.
- playlist jangan penuh sama lagu sendiri.
- gunakan proxy residensial biar captcha lebih sedikit.
- log file bakal bantu kamu tahu akun mana yang error.
