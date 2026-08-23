#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting AI BioMed Assistant..."
exec streamlit run app.py
