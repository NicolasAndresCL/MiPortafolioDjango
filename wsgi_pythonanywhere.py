# ─── wsgi_pythonanywhere.py ────────────────────────────────────────────────────
# Copia el contenido de este archivo al archivo WSGI de PythonAnywhere:
# /var/www/nicolasandrescl_pythonanywhere_com_wsgi.py
#
# O configura en el panel de PythonAnywhere:
#   Source code: /home/nicolasandrescl/Portafolio/backend/MiPortafolioDjango
#   Working directory: /home/nicolasandrescl/Portafolio/backend/MiPortafolioDjango
#   WSGI configuration file: apuntar a este archivo
# ──────────────────────────────────────────────────────────────────────────────

import os
import sys

# Ruta al proyecto Django
path = '/home/nicolasandrescl/Portafolio/backend/MiPortafolioDjango'
if path not in sys.path:
    sys.path.insert(0, path)

# Activar el entorno virtual
activate_this = '/home/nicolasandrescl/Portafolio/backend/MiPortafolioDjango/env/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_project.settings.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
