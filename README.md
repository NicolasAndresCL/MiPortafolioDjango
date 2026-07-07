# Portafolio Backend — Django REST Framework

Backend modular de mi portafolio personal, construido con **Django 5** y **Django REST Framework**. Expone una API pública y documentada para gestionar proyectos, habilidades, experiencia laboral y mensajes de contacto, integrada con un frontend en **React/Vite**.

Desplegado en [PythonAnywhere](https://nicolasandrescl.pythonanywhere.com) · Documentación: `/api/schema/swagger-ui/`

---

## Stack

| Tecnología | Uso |
|---|---|
| **Django 5.2** | Framework web y ORM |
| **Django REST Framework** | ViewSets, serializers, permisos |
| **drf-spectacular** | OpenAPI 3 + Swagger UI personalizado |
| **SimpleJWT** | Autenticación JWT (acceso 30 min, refresh 1 día) |
| **django-environ** | Variables de entorno desde `.env` |
| **Pillow** | Imágenes de proyectos y logos de habilidades |
| **SQLite** | Base de datos (local y producción PythonAnywhere) |

---

## Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/projects/` | GET | Lista proyectos (público) |
| `/api/projects/{id}/` | GET | Detalle de proyecto |
| `/api/skills/` | GET | Lista habilidades (público) |
| `/api/experience/` | GET | Lista experiencia laboral con highlights anidados (público) |
| `/api/experience-highlights/` | GET | Gestión individual de highlights de experiencia |
| `/api/contacto/` | POST | Recibe mensaje del formulario de contacto |
| `/api/schema/swagger-ui/` | GET | Documentación interactiva |
| `/api/schema/redoc/` | GET | Documentación ReDoc |
| `/api/token/` | POST | Login JWT |
| `/api/token/refresh/` | POST | Renovar token |
| `/admin/` | GET | Panel administrativo |

Escritura (POST/PUT/DELETE) requiere autenticación JWT.

---

## Settings modular

```
portfolio_project/settings/
├── base.py         # Configuración compartida (apps, middleware, DRF, JWT, email)
├── development.py  # DEBUG=True, email por consola, CORS local
├── production.py   # DEBUG=False, CORS desde env, headers de seguridad
└── testing.py      # SQLite en memoria, sin .env requerido
```

`manage.py` usa `settings.development` por defecto.
`wsgi.py` usa `settings.production` por defecto.

---

## Variables de entorno

Crea un `.env` en la raíz del backend (ver `.env.example`):

```bash
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMBED_REACT=False

EMAIL_HOST_USER=tu@gmail.com
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx
DEFAULT_FROM_EMAIL=tu@gmail.com
CONTACT_RECIPIENT_EMAIL=tu@gmail.com
```

`EMBED_REACT=True` sirve el build de React desde `/`. Con `False` redirige a Swagger UI.

---

## Correr en local

```bash
# Activar entorno virtual
.\env\Scripts\Activate.ps1        # Windows
source env/bin/activate            # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Backend disponible en **http://localhost:8000**

Para crear un superusuario y acceder al admin:

```bash
python manage.py createsuperuser
```

---

## Tests

```bash
python manage.py test portfolio_app --settings=portfolio_project.settings.testing
```

Suite actual: **40 tests**

| Clase | Tests |
|---|---|
| `ProjectModelTest` | Creación, `__str__`, campos opcionales |
| `SkillModelTest` | Creación, `__str__`, nivel por defecto, categoría opcional |
| `ExperienceModelTest` | Creación, `is_current` según `end_date`, `__str__`, ordenamiento |
| `ExperienceHighlightModelTest` | Creación + relación, ordenamiento, `__str__` |
| `ProjectAPITest` | List, retrieve, ordenamiento, auth requerida para crear |
| `SkillAPITest` | List, retrieve, ordenamiento por nivel, auth requerida para crear |
| `ExperienceAPITest` | List, retrieve con highlights anidados, `is_current`, auth, ordenamiento |
| `ExperienceHighlightAPITest` | List, retrieve, auth requerida para crear, ordenamiento |
| `ContactAPITest` | Éxito, email enviado, campos faltantes, JSON inválido, solo POST |

---

## CI/CD

**`.github/workflows/ci.yml`** — en cada push/PR:
- Python 3.12, instala dependencias, corre los 40 tests

**`.github/workflows/deploy.yml`** — en push a `main`:
- SSH a PythonAnywhere: `git pull`, `pip install`, `migrate`, `collectstatic`
- Recarga la webapp via PythonAnywhere API

Secrets requeridos en GitHub:

| Secret | Descripción |
|---|---|
| `PA_USERNAME` | Usuario de PythonAnywhere |
| `PA_PASSWORD` | Contraseña de PythonAnywhere |
| `PA_API_TOKEN` | API Token (Account → API Token en PA) |

---

## Despliegue en PythonAnywhere

1. Clona el repo en `/home/nicolasandrescl/Portafolio/`
2. Crea el entorno virtual e instala `requirements.txt`
3. Configura el archivo WSGI del panel de PA apuntando a `wsgi_pythonanywhere.py`
4. Agrega las variables de entorno en el `.env` del servidor
5. Ejecuta `python manage.py migrate` y `python manage.py collectstatic`
6. Recarga la webapp desde el panel

Con CI/CD configurado, los pasos 1 y en adelante se automatizan en cada `git push` a `main`.

---

**Nicolás Andrés Cano Leal**
LiveOps & BizOps | Python Backend Developer | Data Automation
