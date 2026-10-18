# Changelog

Todos los cambios relevantes del portafolio (backend Django + frontend React embebido) se
documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa
[Versionado Semántico](https://semver.org/lang/es/). Las versiones anteriores a 2.0.0 no tienen
tag en git; sus entradas se reconstruyeron desde el historial de commits.

## [2.0.1] — 2026-10-18

Un solo titular en los tres canales que ve un reclutador: portafolio, CV y LinkedIn.

### Cambiado
- Titular oficial, igual al de LinkedIn: **Backend Engineer → SRE | Python · Django · Kubernetes ·
  Terraform · CI/CD**. Reemplaza "Backend Python Developer | Automation & Reliability" (tarjeta del
  avatar) y "Backend Python Developer · DevOps & Reliability" (CV ES/EN).
- Tarjeta del avatar: rol y stack en dos líneas, y "Único desarrollador del equipo de operaciones ·
  PedidosYa" en lugar de un lema genérico.
- "Sobre mí" reescrito con los mismos hechos que el Perfil del CV (rol actual en PedidosYa, servicios en
  producción, CI/CD e IaC, objetivo SRE).
- CV ES/EN: titular y primera frase del Perfil; PDF regenerados (siguen en 2 páginas).
- Versión 2.0.1 en la API (OpenAPI), Helm (`appVersion` 2.0.1, chart 0.2.1) y footer.

## [2.0.0] — 2026-10-17

Rediseño visual del frontend con un sistema de temas. El contrato de la API no cambia; el salto
de versión mayor refleja que la identidad visual del portafolio se reemplaza por completo.

### Añadido
- **Sistema de 3 temas** seleccionables desde un botón fijo en la esquina superior derecha
  (Radix `DropdownMenu` con `RadioGroup`):
  - **Cian** (por defecto): medianoche profundo `#070b14`, aurora cian `#22d3ee` → violeta
    `#a78bfa`, nombre en degradado, superficies tipo vidrio con brillo; tipografía Space Grotesk
    + JetBrains Mono.
  - **Violeta**: tema claro, blanco nube, violeta `#7c4dff`, rojo `#e63946` y dorado `#ffbe0b`.
  - **Ámbar**: oscuro brasa `#130d0a`, texto hueso `#efe6d6`, naranja óxido `#d9622b`, titulares
    en Cinzel.
- Temas implementados con `createTheme` de Stitches: el tema base vive en `:root` (Cian) y las
  clases `theme-violeta` / `theme-ambar` se aplican sobre `<html>`.
- **Violeta** usa Fredoka en los titulares; las cuatro fuentes (Space Grotesk, Fredoka, Cinzel,
  JetBrains Mono) se cargan en una sola petición a Google Fonts.
- Persistencia de la elección en `localStorage` (clave `portafolio-theme`); si el navegador la
  bloquea, el sitio sigue funcionando con Cian.
- Versión visible en el footer (`v2.0.0`), inyectada por Vite desde `package.json`.
- Script inline que aplica la clase del tema antes de montar React, para evitar el parpadeo del
  tema por defecto al recargar. Va en `templates/index.html` (lo que sirve Django en producción)
  y en el `index.html` de Vite (desarrollo).

### Cambiado
- `SPECTACULAR_SETTINGS['VERSION']` de la API (Swagger/OpenAPI) pasa a `2.0.0`.
- Chart de Helm: `appVersion` `2.0.0` (versión del chart `0.2.0`).

### Eliminado
- Paleta anterior "VSCode Dark+" del frontend (queda en el historial de git).

## [1.0.0] — 2026-09-27

Línea base reconstruida desde el historial (mayo–septiembre de 2026).

### Añadido
- CV 2026 bilingüe (ES/EN) generado desde HTML, servido en URLs estables `/cv/` y `/cv/en/`;
  certificaciones 2026.
- CD con Jenkins en Docker (build → GHCR opcional → deploy a un stack local → healthcheck →
  smoke test), aislado de la base de producción.
- Type checking con mypy + django-stubs en el CI.
- Experiencia laboral (modelo, API con highlights anidados y tests).
- Stack de robustez de "All in Django": settings tipados con pydantic-settings, paginación,
  throttling, `/healthz/`, gunicorn + WhiteNoise, Docker multi-stage, Terraform y Helm
  demostrativos.
- Comando `reset_sequences` y runbook de migración de SQLite a PostgreSQL (Neon PG16).

### Cambiado
- Settings modulares (`base` / `development` / `production` / `testing`), vistas y URLs
  limpias, CI en GitHub Actions.
- El CD pasa de GitHub Actions a Jenkins (`build.yml` / `deploy.yml` movidos a
  `.github/workflows-disabled/`).
- Frontend embebido regenerado: render resiliente ante fallos de la API, paginación completa y
  menú responsive con Radix `DropdownMenu`.

### Corregido
- `docker compose` sirve el frontend embebido igual que en producción.
- `templates/` antes que `dist/` en `DIRS` para no servir el `index.html` crudo de Vite.

## Pre-1.0 — 2025

Primeras versiones: API REST con DRF y JWT (SimpleJWT), Swagger UI personalizado con
drf-spectacular, formulario de contacto por email e integración del build de React/Vite
(Radix Themes + Stitches) servido por Django.

[2.0.0]: https://github.com/NicolasAndresCL/MiPortafolioDjango/compare/cc737d7...HEAD
[1.0.0]: https://github.com/NicolasAndresCL/MiPortafolioDjango/commit/cc737d7
