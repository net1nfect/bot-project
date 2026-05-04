#!/usr/bin/env bash

# Setup sederhana untuk lingkungan eksperimen.
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
