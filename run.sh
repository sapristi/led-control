#! /bin/bash
cd "$(dirname "$0")"
echo "RUNNING with $1 in $(pwd)"
source .venv/bin/activate
python -m ledcontrol --seconds 600 --led-count 50 $1
