# Migración de SQLite → PostgreSQL (Neon) en PythonAnywhere

Procedimiento **one-time** para pasar el portafolio de SQLite a PostgreSQL sin perder los
datos existentes (proyectos, skills, experiencia).

El código soporta ambos motores: si `DATABASE_URL` está definido usa PostgreSQL
(`dj-database-url` + `psycopg`), y si no, SQLite. Ver `portfolio_project/settings/base.py`.

> **Por qué un Postgres externo y no el de PythonAnywhere:** PA solo ofrece **Postgres 12**,
> y **Django 5.2 requiere Postgres 14+** (`NotSupportedError: PostgreSQL 14 or later is
> required`). Por eso se usa un Postgres gestionado externo con versión 14+ — aquí **Neon**
> (PG16, free tier). Como la cuenta de PA es de pago, puede conectarse a hosts externos.

Rutas reales en el servidor: proyecto en `~/MiPortafolioDjango`, virtualenv
`MiPortafolioDjango_env`.

---

## 0. Antes de empezar

- **Despliega primero el código nuevo** (rama `feat/backend-robusto`): en la consola,
  `git fetch origin && git checkout feat/backend-robusto && pip install -r requirements.txt`.
  Ese código es el que lee `DATABASE_URL`.
- **`SECRET_KEY` fuerte** en el `.env` (≥32 chars, sin `django-insecure`), o `production.py`
  aborta el arranque. Genera una: `python -c "from django.core.management.utils import
  get_random_secret_key; print(get_random_secret_key())"`.

## 1. Crear la base en Neon (PostgreSQL 16)

1. [neon.tech](https://neon.tech) → crea cuenta (gratis, GitHub/Google).
2. **Create project** → Postgres **16**, región **AWS US East** (la más cercana a PA US).
3. Copia el **connection string** que entrega Neon:

   ```
   postgresql://usuario:password@ep-xxxx-yyyy.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

   Neon crea la base (`neondb`) y el usuario automáticamente; no hace falta `CREATE DATABASE`.

## 2. Volcar los datos actuales (¡todavía en SQLite!)

Con `DATABASE_URL` **aún ausente/comentado** del `.env` (para que lea la SQLite actual):

```bash
cd ~/MiPortafolioDjango

python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude contenttypes --exclude auth.permission \
  --exclude admin.logentry --exclude sessions.session \
  --indent 2 --output datadump.json
```

> Se excluyen `contenttypes`/`permissions`/`logentry`/`sessions` para evitar conflictos al
> cargar. El contenido (`portfolio_app.*`) y los usuarios (`auth.user`) sí se vuelcan. Las
> imágenes viven en `media/` (no en la DB), así que no se tocan.

## 3. Apuntar a Neon

Pon en el `.env` de producción el connection string de Neon (paso 1):

```
DATABASE_URL=postgresql://usuario:password@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

> El `?sslmode=require` es obligatorio en Neon. Si la password tuviera caracteres especiales
> (`@ : / #`), URL-encodéalos:
> `python -c "from urllib.parse import quote; print(quote(input(), safe=''))"`.

## 4. Crear el esquema y cargar los datos

```bash
python manage.py migrate            # "Applying ... OK" contra Neon (base vacía)
python manage.py loaddata datadump.json
```

## 5. Resetear las secuencias (crítico en Postgres)

Tras un `loaddata` con PKs explícitas, los autoincrementos de Postgres quedan desactualizados
y el próximo alta daría `duplicate key`. Se corrigen con el comando incluido:

```bash
python manage.py reset_sequences portfolio_app auth
```

(En SQLite este comando es un no-op seguro; solo actúa sobre Postgres.)

## 6. Verificar y recargar

```bash
python manage.py showmigrations | tail
python manage.py shell -c "from portfolio_app.models import Project, Skill; print(Project.objects.count(), Skill.objects.count())"
```

Si el login de admin no funciona (el volcado puede tener una contraseña anterior):
`python manage.py changepassword <usuario>`.

Recarga la webapp desde el panel Web. Comprueba:

- `https://nicolasandrescl.pythonanywhere.com/healthz/` → `{"status": "ok"}`
- `https://nicolasandrescl.pythonanywhere.com/api/projects/` → tus proyectos, paginados.

## 7. Limpieza

```bash
rm datadump.json     # no dejar el volcado con datos en el servidor
```

A partir de aquí sigues gestionando el contenido por Swagger, pero ahora contra Neon. Para
volver a SQLite bastaría con comentar `DATABASE_URL`.

> Nota Neon free tier: la base **se suspende tras inactividad** y despierta en ~1s en la
> primera consulta. Sin impacto real para un portafolio.
