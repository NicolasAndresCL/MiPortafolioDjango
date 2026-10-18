#!/usr/bin/env bash
# Reproduce el CI (.github/workflows/ci.yml) sobre un clon limpio de HEAD: el runner solo ve lo
# versionado, así que se prueba eso y no el working copy.
#   Python 3.12 (el del CI) → pip install -r requirements-dev.txt → mypy → pytest (cobertura en pyproject)
# Usa python3.12 / `py -3.12` si existe; si no, corre los mismos pasos en un contenedor
# python:3.12-slim (Linux, como el runner) que se borra al terminar.
# Uso: bash scripts/verificar.sh
set -euo pipefail

REPO="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "==> Clon limpio de HEAD ($(git -C "$REPO" rev-parse --short HEAD))"
git clone -q "$REPO" "$WORK/repo"

PASOS='set -e
python --version
python -m venv /tmp/venv
/tmp/venv/bin/python -m pip install -q --upgrade pip
echo "==> pip install -r requirements-dev.txt"
/tmp/venv/bin/python -m pip install -q -r requirements-dev.txt
echo "==> mypy portfolio_app portfolio_project"
/tmp/venv/bin/python -m mypy portfolio_app portfolio_project
echo "==> pytest"
/tmp/venv/bin/python -m pytest -q'

PY=""
if command -v python3.12 >/dev/null; then PY="python3.12"
elif py -3.12 --version >/dev/null 2>&1; then PY="py -3.12"
fi

if [ -n "$PY" ]; then
  cd "$WORK/repo"
  $PY -m venv "$WORK/venv"
  VENV_BIN="$WORK/venv/bin"; [ -d "$VENV_BIN" ] || VENV_BIN="$WORK/venv/Scripts"
  "$VENV_BIN/python" -m pip install -q --upgrade pip
  "$VENV_BIN/python" -m pip install -q -r requirements-dev.txt
  "$VENV_BIN/python" -m mypy portfolio_app portfolio_project
  "$VENV_BIN/python" -m pytest -q
else
  echo "==> Sin Python 3.12 local: se usa el contenedor python:3.12-slim"
  # MSYS_NO_PATHCONV: en Git Bash evita que /repo se convierta en una ruta de Windows.
  MSYS_NO_PATHCONV=1 docker run --rm -v "$(cd "$WORK/repo" && pwd -W 2>/dev/null || pwd):/repo" \
    -w /repo python:3.12-slim bash -c "$PASOS"
fi

echo "OK: el CI debería pasar con este HEAD."
