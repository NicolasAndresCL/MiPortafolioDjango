import json
import os
from django.conf import settings


def vite_assets(request):
    """Inyecta los nombres de assets del build de Vite en el contexto del template."""
    manifest_path = os.path.join(
        settings.BASE_DIR, 'static', 'frontend', 'dist', '.vite', 'manifest.json'
    )
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        entry = manifest.get('index.html', {})
        return {
            'vite_js': entry.get('file', ''),
            'vite_css': entry.get('css', [''])[0] if entry.get('css') else '',
        }
    except (FileNotFoundError, json.JSONDecodeError):
        return {'vite_js': '', 'vite_css': ''}
