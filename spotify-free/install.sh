#!/bin/bash
set -e

echo "=== Spotify Bot Free - VPS Setup ==="

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git screen curl
sudo apt install -y \
    libnss3 libnspr4 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libasound2 libpango-1.0-0 libcairo2

mkdir -p ~/spotify-bot-free
cd ~/spotify-bot-free
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 -m playwright install chromium
python3 -m playwright install-deps
mkdir -p config data/cookies logs

echo "Setup complete! Next steps:"
echo "1. Add proxies to config/proxies.txt"
echo "2. Add playlist metadata to config/playlist.json"
echo "3. Run: source venv/bin/activate && python scripts/account_generator.py --count 5"
echo "4. Run: python scripts/session_initializer.py"
echo "5. Run: python src/main.py"
