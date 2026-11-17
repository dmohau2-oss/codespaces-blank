#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

cd frontend
npm install
npm run build
cd "$PROJECT_ROOT"

python -m src.main --input data/sample_input.csv --output output/processed.csv

nohup uvicorn src.api:app --host 0.0.0.0 --port 8000 \
  >/tmp/data_app.log 2>&1 &

echo "Deployment complete. App available at http://127.0.0.1:8000"
