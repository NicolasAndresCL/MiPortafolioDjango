#!/usr/bin/env bash
# Reproduce el CI (.github/workflows/ci.yml) sobre un clon limpio de HEAD: el runner solo ve lo
# versionado, así que se prueba eso y no el working copy.
#   Python 3.12 (el del CI) → pip install -r requirements-dev.txt → mypy → pytest (cobertura en pyproject)
# Uso: bash scripts/verificar.sh   (requiere `py -3.12` en Windows o `python3.12` en Linux)
set -euo pipefail

REPO="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PY="$(command -v python3.12 || true)"
if [ -z "$PY" ] && command -v py >/dev/null; then PY="py -3.12"; fi
[ -n "$PY" ] || { echo "Falta Python 3.12 (la versión del CI)"; exit 1; }

echo "==> Clon limpio de HEAD ($(git -C "$REPO" rev-parse --short HEAD))"
git clone -q "$REPO" "$WORK/repo"
cd "$WORK/repo"

echo "==> venv nuevo con $($PY --version)"
$PY -m venv "$WORK/venv"
VENV_BIN="$WORK/venv/bin"; [ -d "$VENV_BIN" ] || VENV_BIN="$WORK/venv/Scripts"

echo "==> pip install -r requirements-dev.txt"
"$VENV_BIN/python" -m pip install -q --upgrade pip
"$VENV_BIN/python" -m pip install -q -r requirements-dev.txt

echo "==> mypy portfolio_app portfolio_project"
"$VENV_BIN/python" -m mypy portfolio_app portfolio_project

echo "==> pytest"
"$VENV_BIN/python" -m pytest -q

echo "OK: el CI debería pasar con este HEAD."
