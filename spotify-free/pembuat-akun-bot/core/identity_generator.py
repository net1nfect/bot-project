"""Generator identitas sintetis untuk eksperimen registrasi pengguna.

Modul ini menyediakan data profil yang memenuhi syarat usia dan kompleksitas
kata sandi untuk memetakan lapisan validasi identitas pada registrasi.
"""

from __future__ import annotations

import random
import string
from typing import Dict

from faker import Faker

fake = Faker("id_ID")

NAME_DATABASE = {
    "first_names": [
        "Ahmad", "Rizki", "Siti", "Dewi", "Budi", "Rina", "Agus", "Putri",
        "Hendra", "Lulu", "Andi", "Fitri", "Rani", "Dian", "Yudha",
    ],
    "last_names": [
        "Saputra", "Pratama", "Hidayat", "Permana", "Kusuma", "Suryani",
        "Wijaya", "Sutanto", "Ramadhan", "Pratiwi", "Nur", "Sari",
    ],
}

PASSWORD_SYMBOLS = "!@#$%^&*()-_+="


def _random_username(length: int = 12) -> str:
    """Buat username unik yang hanya berisi huruf kecil dan angka."""
    choices = string.ascii_lowercase + string.digits
    return "".join(random.choice(choices) for _ in range(length))


def _random_password(length: int = 12) -> str:
    """Buat kata sandi kompleks yang memenuhi persyaratan eksperimen."""
    parts = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(PASSWORD_SYMBOLS),
    ]
    remaining = [
        random.choice(string.ascii_letters + string.digits + PASSWORD_SYMBOLS)
        for _ in range(max(0, length - len(parts)))
    ]
    password_chars = parts + remaining
    random.shuffle(password_chars)
    return "".join(password_chars)


def _random_birthdate() -> str:
    """Pilih tanggal lahir dalam rentang 1990-2000 untuk memastikan usia > 18."""
    year = random.randint(1990, 2000)
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month in {4, 6, 9, 11}:
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    return f"{year:04d}-{month:02d}-{day:02d}"


def _random_gender() -> str:
    """Pilih jenis kelamin secara acak untuk menguji variasi field registrasi."""
    return random.choice(["male", "female"])


def generate_identity() -> Dict[str, str]:
    """Menghasilkan identitas sintetis terstruktur untuk pengujian registrasi."""
    first_name = random.choice(NAME_DATABASE["first_names"])
    last_name = random.choice(NAME_DATABASE["last_names"])
    full_name = f"{first_name} {last_name}"

    username = _random_username(12)
    password = _random_password(12)
    birthdate = _random_birthdate()
    gender = _random_gender()

    return {
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "password": password,
        "birthdate": birthdate,
        "gender": gender,
        "display_name": full_name,
    }
