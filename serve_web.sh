#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

"$ROOT_DIR/.venv/bin/python" -m pygbag --build "$ROOT_DIR"
"$ROOT_DIR/.venv/bin/python" "$ROOT_DIR/tools/patch_pygbag_index.py"

cd "$ROOT_DIR"
exec python3 -m http.server 8000 -d build/web