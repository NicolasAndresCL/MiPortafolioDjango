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
| **pytest + pytest-cov** | Suite de tests (49 tests, ~91% cobertura) |
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
| `/cv/` · `/cv/en/` | GET | Redirige al CV en PDF (español · inglés); sin auth |
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

Con `EMBED_REACT=True` (igual que en PythonAnywhere) sirve el frontend en
**http://localhost:8000** y el CV en `/cv/` y `/cv/en/`. Limitación: el bundle de React
llama a la API de **producción** (`VITE_API_BASE_URL` se fija en el build) y producción no
acepta CORS desde `localhost`, así que las secciones de datos aparecen vacías y los botones del
CV abren producción. Sirve para validar imagen, estáticos, layout y rutas; no el contenido.
`docker compose down` para detenerlo (`-v` borra también el volumen de Postgres).

### Migrar de SQLite a PostgreSQL

Si defines `DATABASE_URL` el backend usa Postgres; si no, SQLite. Para migrar los datos
existentes sin perderlos (dump → loaddata → reset de secuencias con `manage.py
reset_sequences`), sigue el runbook: [`docs/migracion_postgres.md`](docs/migracion_postgres.md).

## CV en PDF

El CV **no se genera en el servidor**: su fuente es HTML imprimible versionado en
[`docs/cv/`](docs/cv/) (`cv_es.html`, `cv_en.html`, `cv.css`) y el PDF se imprime en local
con Edge/Chrome headless. PythonAnywhere solo sirve un archivo estático: cero CPU y ninguna
dependencia nueva.

```bash
python scripts/build_cv.py      # → portfolio_app/static/portfolio_app/docs/NicolasCano_CV_{ES,EN}.pdf
```

Para publicar un cambio: editar el HTML → `build_cv.py` → commit de HTML + PDF → en el
servidor `git pull` + `collectstatic` + recargar la webapp. Las URLs públicas son estables
(`/cv/`, `/cv/en/`) y no dependen del build del frontend; la URL histórica
`/NicolasCano_BackendDeveloper_CV.pdf` redirige a `/cv/` (antes el catch-all del SPA la
respondía con `index.html`, y el "PDF" descargado era HTML).

---

## Tests y type checking

```bash
pytest                          # 49 tests + reporte de cobertura (~91%)
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
| `CVDownloadTest` | `/cv/` ES/EN, idioma inválido 404, URL histórica → 301, PDFs presentes |
| `ContactAPITest` | Éxito, email enviado, campos faltantes, JSON inválido, solo POST |

---

## Contenedorización e IaC (demostrativo)

Coexiste con el deploy real de PythonAnywhere; no lo reemplaza.

| Recurso | Qué hace |
|---|---|
| `Dockerfile` | Imagen multi-stage, usuario no-root, gunicorn + WhiteNoise, `collectstatic` en build |
| `docker-compose.yml` | Postgres 16 (healthcheck) + API; migraciones vía `entrypoint.sh` |
| `docker-compose.deploy.yml` | Corre la imagen publicada en GHCR (lo usa el CD de Jenkins) |
| `jenkins/` + `Jenkinsfile` | Servidor Jenkins en Docker + pipeline de CD (build → GHCR → deploy) |
| `terraform/` | EC2 + RDS Postgres + security groups + `cloud-init` (validado con `terraform validate`) |
| `helm/portafolio/` | Deployment (initContainer de migraciones) + StatefulSet Postgres + ConfigMap/Secret/Ingress |

---

## CI/CD

Reparto: **GitHub Actions = CI** (tests) · **Jenkins = CD** (build + deploy).

### CI — GitHub Actions
**`.github/workflows/ci.yml`** — en cada push/PR:
- Python 3.12, instala `requirements-dev.txt`, corre `mypy` (type check) y `pytest` con cobertura, y sube el `coverage.xml`

### CD — Jenkins en Docker
Job **`portafolio-cd`** en un Jenkins containerizado que ejecuta el `Jenkinsfile` (pipeline
declarativo) y despliega un **stack demostrativo local** en http://localhost:8001:
1. **Proteger DB de producción** — aborta si alguna variable del build contiene una URL de Neon
2. **Test (gate)** — mypy + pytest en un contenedor efímero `python:3.12-slim`
3. **Build** — imagen Docker (`ghcr.io/<owner>/portafolio-backend:<commit>`)
4. **Push GHCR** — opcional (parámetro `PUBLISH_GHCR`, apagado por defecto)
5. **Deploy** — `docker-compose.deploy.yml` (api + Postgres propio)
6. **Healthcheck** — estado de salud de Docker; falla el build si no queda `healthy`
7. **Smoke test** — `/healthz/`, `/cv/`, `/cv/en/` y `/` dentro del contenedor, y verifica que la
   API use el Postgres local

**El pipeline no toca producción**: `DATABASE_URL` está fija al Postgres del compose de deploy (no
se lee del entorno) y no existe credencial de base de datos. Producción (PythonAnywhere + Neon) se
despliega a mano. Setup, credenciales y triggers en [`jenkins/README.md`](jenkins/README.md).
Trigger por `pollSCM` (Jenkins local no recibe webhooks).

Los antiguos `build.yml`/`deploy.yml` (CD en GitHub Actions) quedaron en
`.github/workflows-disabled/` como referencia.

---

## Despliegue en PythonAnywhere

1. Clona el repo en `/home/nicolasandrescl/MiPortafolioDjango/` (venv `MiPortafolioDjango_env`)
2. Crea el entorno virtual e instala `requirements.txt`
3. Configura el archivo WSGI del panel de PA apuntando a `wsgi_pythonanywhere.py`
4. Agrega las variables de entorno en el `.env` del servidor
5. Ejecuta `python manage.py migrate` y `python manage.py collectstatic`
6. Recarga la webapp desde el panel

El deploy a PythonAnywhere es **manual** (`git pull` + pasos 5–6): el antiguo `deploy.yml` quedó
desactivado en `.github/workflows-disabled/` y el CD con Jenkins apunta al stack Docker, no a PA.

---

**Nicolás Andrés Cano Leal**
LiveOps & BizOps | Python Backend Developer | Data Automation
