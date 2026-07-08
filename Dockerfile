# syntax=docker/dockerfile:1

# ---- Stage 1: builder — instala dependencias en un prefijo aislado ----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ---- Stage 2: runtime — imagen mínima, usuario no-root ----
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=portfolio_project.settings.production

WORKDIR /app

# Librerías de runtime para lxml + usuario sin privilegios
RUN apt-get update \
    && apt-get install -y --no-install-recommends libxml2 libxslt1.1 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app && useradd --system --gid app --home-dir /app app

# Dependencias ya construidas
COPY --from=builder /install /usr/local

COPY . .

# Recolecta estáticos (WhiteNoise los sirve). SECRET_KEY dummy solo para el build.
RUN SECRET_KEY="build-only-dummy-key-not-used-at-runtime-0000000000" \
    python manage.py collectstatic --noinput

RUN chown -R app:app /app
USER app

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]
CMD ["gunicorn", "portfolio_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
