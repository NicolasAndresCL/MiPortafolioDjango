# Nicolás Andrés Cano Leal
**Backend Python Developer · Automation & Reliability · LiveOps/BizOps**

Rancagua, Chile · [nicolas.cano.leal@gmail.com](mailto:nicolas.cano.leal@gmail.com)
[GitHub](https://github.com/NicolasAndresCL) · [LinkedIn](https://www.linkedin.com/in/nicolas-andres-cano-leal) · [Portafolio](https://nicolasandrescl.pythonanywhere.com)

> Este archivo es el **borrador de contenido** para el CV en PDF. No es el PDF final:
> Nicolás lo maqueta a mano y luego sincroniza el PDF resultante en las dos ubicaciones
> servidas (`portfolio_app/static/portfolio_app/docs/` y `frontend/.../public/`).

---

## Resumen profesional

Desarrollador Backend Python que empezó construyendo APIs y hoy mira el panorama completo:
no solo cómo se construye un sistema, sino cómo se opera, se automatiza y se mantiene en pie
bajo carga real. Actualmente en un rol de operaciones (LiveOps/BizOps) donde soy el único
desarrollador del equipo: reemplazo procesos manuales y planillas por servicios Python
modernos, testeados y mantenibles. Me especializo en Django y DRF para APIs limpias y bien
documentadas, con foco creciente en confiabilidad e infraestructura como código, apuntando a
una carrera en Site Reliability Engineering (SRE).

---

## Experiencia laboral

### PedidosYa — Live Performance Agent (LiveOps / BizOps)
**Rancagua, Chile · agosto 2025 – Presente**

Único desarrollador de un equipo de operaciones. Responsable en solitario de la evolución de
las herramientas internas de automatización que sostienen la operación en tiempo real.

- Automatización y evolución del bot interno de operaciones a través de 10 versiones
  (v4.0 → v5.0), con 144 commits documentados bajo convenciones profesionales.
- Cobertura de 481 tests automatizados, garantizando estabilidad en cada release y
  operación desatendida.
- Arquitectura en capas: lógica pura separada de efectos secundarios (Selenium, red,
  BigQuery), 100% testeable sin abrir un navegador.
- Orquestación de ~10 engines concurrentes en hilos para gestión de tareas LiveOps en
  tiempo real (motores stagnant, reporting, alertas, watchdogs).
- Diseño de un cooldown con reserva atómica para cerrar una condición de carrera
  check-then-act entre motores concurrentes.
- Sistema anti-duplicidad entre operadores mediante heartbeat en Google Sheet.
- Optimización real de rendimiento: singleton con caché TTL que redujo llamadas a Sheets de
  21 round-trips a 1 (~16 min → <1 min); cuello de botella global de ~37 min → ~10 min.
- Ingeniería inversa del DOM (React/Recharts) para extraer datos sin API disponible.

*Stack: Python, Django, Docker, Jenkins, Streamlit, Selenium, SQLite, Google Sheets API, BigQuery.*

---

## Proyectos destacados

Catálogo completo y en vivo en el portafolio. Selección representativa:

- **All in Django** — Reimplementación Django + DRF con IaC completa: PostgreSQL en
  producción, Docker multi-stage no-root, Terraform (EC2+RDS), Helm (Deployment +
  StatefulSet Postgres + Ingress). CI en GitHub Actions, endurecimiento de seguridad
  (auth por token, rate limiting, `check --deploy` limpio). 130 tests, ~83% cobertura.
- **DailyDevLog** — Dashboard técnico para registrar y exportar tareas de desarrollo.
  Migrado de PySide6 a frontend React (Radix + Stitches); backend con DRF, JWT y Pytest.
- **SparkTrace (Spark Trace Backend)** — Backend modular para carga masiva y trazabilidad
  reproducible con DRF, comandos desacoplados, PySpark y documentación bilingüe.
- **Arcade DRF + GraphQL** — API REST y GraphQL con JWT, documentación OpenAPI avanzada
  (drf-spectacular) y arquitectura escalable.
- **Tiendita de Marian (Backend + Frontend)** — E-commerce con API Django REST segura (JWT,
  MySQL, Pytest) y frontend React desacoplado.
- **CRUD Backend Escalable (FastAPI)** — API de alto rendimiento con FastAPI, SQLAlchemy,
  MySQL y Pytest.
- **Workshift Analytics Pro / OmniSched v2.1** — Apps Streamlit para gestión y análisis de
  turnos y productividad (SQLite, Plotly, exportación PDF/Excel).
- **API con DRF (Arquitectura Modular)** — API RESTful de clientes/pedidos con validación
  robusta, control de CORS y permisos.

*Repositorios: [github.com/NicolasAndresCL](https://github.com/NicolasAndresCL)*

---

## Habilidades técnicas

- **Lenguajes:** Python (avanzado), JavaScript, SQL, R.
- **Frameworks Backend:** Django, Django REST Framework, FastAPI, Flask.
- **Frontend:** React, Radix Themes + Stitches, Streamlit, NiceGUI, TailwindCSS,
  Shadcn/UI, HTML, CSS.
- **Bases de datos:** PostgreSQL, MySQL, SQLite.
- **Data & Analytics:** Pandas, NumPy, Matplotlib, Power BI, Jupyter.
- **DevOps / IaC:** Docker, Jenkins, GitHub Actions (CI/CD), Terraform, Helm/Kubernetes, AWS.
- **Automatización / Scraping:** Selenium, n8n, BeautifulSoup, VBA→Python.
- **UI escritorio:** PySide6, Tkinter, PyGame.
- **Calidad:** Pytest, drf-spectacular (OpenAPI/Swagger), unittest.mock, coverage.py.
- **Herramientas:** Git/GitHub (conventional commits), VS Code, IntelliJ IDEA.

---

## Formación

- **Ingeniería en Informática** — IP Santo Tomás *(en curso)*.
- **Técnico en Enfermería, Mención Instrumentista Quirúrgico** — INACAP, 2014.
- **Formación autodidacta intensiva** — 2.500+ horas de estudio en desarrollo backend
  Python, arquitectura de software y DevOps.

---

## Roadmap profesional

Objetivo de carrera: **Site Reliability Engineering (SRE)**, con acceso al mercado remoto
internacional. En curso: profundización en Java (segundo lenguaje tipado/compilado),
PostgreSQL en producción, y certificaciones en investigación (Terraform Associate, CKA,
Google Cloud Professional Cloud DevOps Engineer). Filosofía: *sistemas que escalan, se
observan y se recuperan solos.*

> *"El buen software no solo se escribe, se entiende y se evoluciona."*
