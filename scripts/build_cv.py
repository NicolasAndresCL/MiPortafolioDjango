"""Genera los PDF del CV a partir de docs/cv/cv_{es,en}.html.

Se ejecuta en local, no en el servidor: imprime el HTML con Edge o Chrome
headless y deja el PDF como archivo estático. Así PythonAnywhere solo sirve un
archivo (cero CPU, cero dependencias nuevas) y el contenido vive versionado.

    python scripts/build_cv.py

Después: commit de los PDF y `collectstatic` en el servidor.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / 'docs' / 'cv'
OUTPUT_DIR = BASE_DIR / 'portfolio_app' / 'static' / 'portfolio_app' / 'docs'

CVS = {
    'cv_es.html': 'NicolasCano_CV_ES.pdf',
    'cv_en.html': 'NicolasCano_CV_EN.pdf',
}

BROWSER_CANDIDATES = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'msedge', 'google-chrome', 'chromium', 'chromium-browser',
]


def find_browser() -> str:
    for candidate in BROWSER_CANDIDATES:
        path = candidate if Path(candidate).is_file() else shutil.which(candidate)
        if path:
            return path
    sys.exit('No se encontró Edge ni Chrome para imprimir el PDF.')


def render(browser: str, source: Path, target: Path) -> None:
    # Perfil temporal: si el navegador ya está abierto con el perfil normal,
    # headless se engancha a esa instancia y no escribe el PDF. El proceso de
    # crashpad sobrevive unos instantes y bloquea archivos: no fallar al limpiar.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        subprocess.run(
            [
                browser,
                '--headless=new',
                '--disable-gpu',
                '--no-pdf-header-footer',
                f'--user-data-dir={profile}',
                f'--print-to-pdf={target}',
                source.as_uri(),
            ],
            check=True,
            capture_output=True,
            timeout=60,
        )
    # El proceso puede terminar antes de que el PDF quede escrito en disco.
    for _ in range(50):
        if target.is_file() and target.stat().st_size > 0:
            return
        time.sleep(0.2)
    sys.exit(f'El navegador no generó {target.name}.')


def main() -> None:
    browser = find_browser()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for html_name, pdf_name in CVS.items():
        target = OUTPUT_DIR / pdf_name
        target.unlink(missing_ok=True)
        render(browser, SOURCE_DIR / html_name, target)
        print(f'{pdf_name}: {target.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
