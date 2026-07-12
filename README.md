# Portafolio Backend — Django REST Framework

Backend modular de mi portafolio personal, construido con **Django 5** y **Django REST Framework**. Expone una API pública y documentada para gestionar proyectos, habilidades, experiencia laboral y mensajes de contacto, integrada con un frontend en **React/Vite**.

Desplegado en [PythonAnywhere](https://nicolasandrescl.pythonanywhere.com) · Documentación: `/api/schema/swagger-ui/`

---

## Stack

| Tecnología | Uso |
|---|---|
| **Django 5.2 LTS** | Framework web y ORM |
| **Django REST Framework** | ViewSets, serializers, permisos, throttling, paginación |
| **drf-spectacular** | OpenAPI 3 + Swagger UI personalizado |
| **SimpleJWT** | Autenticación JWT (acceso 30 min, refresh 1 día) |
| **pydantic-settings** | Configuración tipada y validada desde `.env` |
| **dj-database-url + psycopg 3** | PostgreSQL en producción, con fallback a SQLite |
| **gunicorn + WhiteNoise** | Servidor WSGI y servido de estáticos en contenedor |
| **Pillow** | Imágenes de proyectos y logos de habilidades |
| **pytest + pytest-cov** | Suite de tests (44 tests, ~91% cobertura) |
| **mypy + django-stubs** | Type checking (en el CI) |
| **Docker · Terraform · Helm** | Contenedorización e IaC (demostrativa) |

### Arquitectura de despliegue

- **PythonAnywhere (deploy real):** virtualenv + WSGI propio, sirviendo sobre **PostgreSQL
  gestionado (Neon PG16)** vía `DATABASE_URL`. El frontend React va embebido (`EMBED_REACT`).
  Sin `DATABASE_URL` el backend cae a SQLite; la seguridad HTTPS está *gated* por entorno.
  > Nota: el Postgres propio de PythonAnywhere es la versión 12 y Django 5.2 requiere 14+, por
  > eso se usa un Postgres externo (Neon). Ver [`docs/migracion_postgres.md`](docs/migracion_postgres.md).
- **Docker / Kubernetes / AWS (demostrativo):** con `DATABASE_URL` a un Postgres propio,
  gunicorn + WhiteNoise sirven la app; Terraform provisiona EC2 + RDS y Helm despliega en K8s.
  Todo **aditivo y configurable por entorno**.

---

## Endpoints

| Endpoint | Método | Descripción |
|---|---|---|
| `/healthz/` | GET | Readiness probe (verifica la DB); sin auth |
| `/api/projects/` | GET | Lista proyectos, paginada (público) |
| `/api/projects/{id}/` | GET | Detalle de proyecto |
| `/api/skills/` | GET | Lista habilidades, paginada (público) |
| `/api/experience/` | GET | Lista experiencia laboral con highlights anidados (público) |
| `/api/experience-highlights/` | GET | Gestión individual de highlights de experiencia |
| `/api/contacto/` | POST | Recibe mensaje del formulario de contacto |
| `/api/schema/swagger-ui/` | GET | Documentación interactiva |
| `/api/schema/redoc/` | GET | Documentación ReDoc |
| `/api/token/` | POST | Login JWT (rate limit 10/min) |
| `/api/token/refresh/` | POST | Renovar token |
| `/admin/` | GET | Panel administrativo |

Escritura (POST/PUT/DELETE) requiere autenticación JWT. Respuestas de lista **paginadas**
(`{count, next, previous, results}`). Rate limiting: anónimo 60/min, autenticado 300/min.

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

# Instalar dependencias (prod + dev)
pip install -r requirements-dev.txt

# Aplicar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Backend disponible en **http://localhost:8000** (SQLite si no defines `DATABASE_URL`).

Para crear un superusuario y acceder al admin:

```bash
python manage.py createsuperuser
```

### Con Docker + PostgreSQL

```bash
docker compose up --build      # levanta db (Postgres) + api (gunicorn)
curl http://localhost:8000/healthz/          # {"status": "ok"}
```

### Migrar de SQLite a PostgreSQL

Si defines `DATABASE_URL` el backend usa Postgres; si no, SQLite. Para migrar los datos
existentes sin perderlos (dump → loaddata → reset de secuencias con `manage.py
reset_sequences`), sigue el runbook: [`docs/migracion_postgres.md`](docs/migracion_postgres.md).

---

## Tests y type checking

```bash
pytest                          # 44 tests + reporte de cobertura (~91%)
mypy portfolio_app portfolio_project   # type checking (django-stubs)
```

Tests configurados en `pyproject.toml` (`DJANGO_SETTINGS_MODULE=...settings.testing`, `--cov`);
`conftest.py` fuerza SQLite. Type checking en `mypy.ini` (django-stubs + drf-stubs, modo laxo);
ambos corren en el CI. Dependencias de dev/typing en `requirements-dev.txt`.

| Clase | Tests |
|---|---|
| `ProjectModelTest` / `SkillModelTest` | Creación, `__str__`, campos por defecto/opcionales |
| `ExperienceModelTest` / `ExperienceHighlightModelTest` | `is_current`, relación, ordenamiento |
| `ProjectAPITest` / `SkillAPITest` | List (paginado), retrieve, ordenamiento, auth para crear |
| `ExperienceAPITest` / `ExperienceHighlightAPITest` | List, retrieve, highlights anidados, auth |
| `HealthCheckTest` / `PaginationTest` | `/healthz/` 200/405, envoltura de paginación |
| `ContactAPITest` | Éxito, email enviado, campos faltantes, JSON inválido, solo POST |

---

## Contenedorización e IaC (demostrativo)

Coexiste con el deploy real de PythonAnywhere; no lo reemplaza.

| Recurso | Qué hace |
|---|---|
| `Dockerfile` | Imagen multi-stage, usuario no-root, gunicorn + WhiteNoise, `collectstatic` en build |
| `docker-compose.yml` | Postgres 16 (healthcheck) + API; migraciones vía `entrypoint.sh` |
| `.github/workflows/build.yml` | Build y push de la imagen a GHCR en tags `v*` |
| `terraform/` | EC2 + RDS Postgres + security groups + `cloud-init` (validado con `terraform validate`) |
| `helm/portafolio/` | Deployment (initContainer de migraciones) + StatefulSet Postgres + ConfigMap/Secret/Ingress |

---

## CI/CD

**`.github/workflows/ci.yml`** — en cada push/PR:
- Python 3.12, instala `requirements-dev.txt`, corre `mypy` (type check) y `pytest` con cobertura, y sube el `coverage.xml`

**`.github/workflows/build.yml`** — en tags `v*`:
- Build de la imagen Docker y push a GHCR (`ghcr.io/<owner>/portafolio-backend`)

**`.github/workflows/deploy.yml`** — en push a `main`:
- SSH a PythonAnywhere: `git pull`, `pip install`, `migrate`, `collectstatic`
- Recarga la webapp via PythonAnywhere API (sin cambios; sigue en SQLite)

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
