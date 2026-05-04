#!/usr/bin/env bash

# Panduan menjalankan eksperimen Spotify Defense Analysis

set -euo pipefail

echo "Spotify Defense Analysis Automation"
echo "===================================="
echo ""

# Aktifkan virtual environment
source .venv/bin/activate

echo "Mode Operasi:"
echo ""
echo "1. Registrasi Akun (Headless):"
echo "   .venv/bin/python main.py --mode registration --workers 1"
echo ""
echo "2. Registrasi Akun (Dengan GUI Chromium - VISUAL MONITORING):"
echo "   .venv/bin/python main.py --mode registration --workers 1 --visual"
echo ""
echo "3. Simulasi Playback (Headless):"
echo "   .venv/bin/python main.py --mode playback --workers 1"
echo ""
echo "4. Simulasi Playback (Dengan GUI - VISUAL MONITORING):"
echo "   .venv/bin/python main.py --mode playback --workers 1 --visual"
echo ""
echo "Opsi Tambahan:"
echo "   --workers <N>        Jumlah worker concurrent (default: 5)"
echo "   --playlist-url <URL> URL playlist Spotify target"
echo ""
echo "Output Eksperimen:"
echo "   - logs/experiment.log          Log event terstruktur JSON"
echo "   - data/sessions/               File sesi browser (.json)"
echo "   - data/fingerprints/           Data fingerprint (reserved)"
echo ""
echo "Contoh:"
echo "   # Run 3 worker registrasi dengan GUI untuk monitoring"
echo "   .venv/bin/python main.py --mode registration --workers 3 --visual"
echo ""
