# Migración de SQLite → PostgreSQL en PythonAnywhere

Procedimiento **one-time** para pasar el portafolio de SQLite a PostgreSQL sin perder los
datos existentes (proyectos, skills, experiencia). Requiere **cuenta de pago** de
PythonAnywhere (necesaria para Postgres y para el acceso SSH/consola).

El código ya soporta ambos motores: si `DATABASE_URL` está definido usa PostgreSQL
(`dj-database-url` + `psycopg`), y si no, SQLite. Ver `portfolio_project/settings/base.py`.

---

## 0. Antes de empezar

- **Despliega primero el código nuevo** (rama `feat/backend-robusto` mergeada a `main` →
  deploy). Ese código es el que soporta `DATABASE_URL`.
- **Verifica que `SECRET_KEY` en el `.env` de producción sea fuerte (≥32 chars** y que no
  empiece con `django-insecure`), porque `settings/production.py` lo valida al arrancar.

## 1. Crear la base PostgreSQL en PythonAnywhere

Panel de PythonAnywhere → pestaña **Databases** → sección **Postgres** →
*Start a Postgres server*. Anota: host, puerto, usuario y contraseña. Crea una base
(p. ej. `portafolio`). El host tendrá la forma:

```
<usuario>-<id>.postgres.pythonanywhere-services.com
```

## 2. Volcar los datos actuales (¡todavía en SQLite!)

En una **consola Bash** de PythonAnywhere, con `DATABASE_URL` **aún ausente** del `.env`
(para que lea la SQLite actual):

```bash
workon <tu-virtualenv>
cd ~/Portafolio/backend/MiPortafolioDjango

python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude contenttypes --exclude auth.permission \
  --exclude admin.logentry --exclude sessions.session \
  --indent 2 --output datadump.json
```

> Se excluyen `contenttypes`/`permissions`/`logentry`/`sessions` para evitar conflictos al
> cargar. Los datos de contenido (`portfolio_app.*`) y los usuarios (`auth.user`) sí se vuelcan.
> Las imágenes viven en `media/` (no en la DB), así que no se tocan.

## 3. Apuntar a PostgreSQL

Añade al `.env` de producción la URL de conexión (con los datos del paso 1):

```
DATABASE_URL=postgres://usuario:password@usuario-XXXX.postgres.pythonanywhere-services.com:PUERTO/portafolio
```

## 4. Crear el esquema y cargar los datos

```bash
python manage.py migrate          # crea las tablas vacías en Postgres
python manage.py loaddata datadump.json
```

## 5. Resetear las secuencias (crítico en Postgres)

Tras un `loaddata` con PKs explícitas, los contadores de autoincremento de Postgres quedan
desactualizados y el próximo alta daría `duplicate key`. Se corrigen con el comando incluido:

```bash
python manage.py reset_sequences            # portfolio_app por defecto
python manage.py reset_sequences portfolio_app auth
```

(En SQLite este comando es un no-op seguro; solo actúa sobre Postgres.)

## 6. Verificar y recargar

```bash
python manage.py showmigrations | tail       # migraciones aplicadas
python manage.py shell -c "from portfolio_app.models import Project, Skill; print(Project.objects.count(), Skill.objects.count())"
```

Recarga la webapp desde el panel (o vía el reload del `deploy.yml`). Comprueba:

- `https://nicolasandrescl.pythonanywhere.com/healthz/` → `{"status": "ok"}`
- `https://nicolasandrescl.pythonanywhere.com/api/projects/` → tus proyectos, paginados.

## 7. Limpieza

```bash
rm datadump.json     # no dejar el volcado con datos en el servidor
```

A partir de aquí sigues gestionando el contenido por Swagger como siempre, pero ahora contra
PostgreSQL. Para volver a SQLite bastaría con quitar `DATABASE_URL` del `.env`.
