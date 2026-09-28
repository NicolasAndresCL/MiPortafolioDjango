# Jenkins (CD) — Portafolio backend

Job **`portafolio-cd`**: ejecuta el `Jenkinsfile` de la raíz del backend y despliega un **stack
demostrativo local** (api + Postgres propio) en **http://localhost:8001**.

El **CI** (tests en cada push/PR) vive en GitHub Actions (`.github/workflows/ci.yml`). Producción
(PythonAnywhere + Neon) se despliega **a mano** y este pipeline **no la toca**.

## Qué controller se usa

El job corre en el **Jenkins compartido** del workspace (`C:\dev\projects\jenkins`, contenedor
`jenkins`, volumen externo `jenkins_home`), el mismo de All in Django. Ahí se crean **por código**,
en `C:\Users\Nicol\jenkins_home\init.groovy.d\`, de forma idempotente:

| Script | Qué hace |
|---|---|
| `70-portafolio-credencial.groovy` | Crea la credencial *Secret text* `portafolio-django-secret-key` desde `secretos/portafolio-django-secret-key.txt` |
| `71-portafolio-job.groovy` | Crea el job `portafolio-cd` (pipeline desde SCM, rama `main`, parámetro `PUBLISH_GHCR`) |

```bash
cd C:\dev\projects\jenkins && docker compose up -d        # UI → http://localhost:8080
```

La `SECRET_KEY` de esa credencial es **propia del stack demostrativo** (generada al azar), no la de
producción. Para rotarla: editar el `.txt` y reiniciar Jenkins.

> La carpeta `jenkins/` de este repo (Dockerfile + compose con contenedor `portafolio-jenkins`) es
> un controller autónomo alternativo, **no el que se usa**. Ocupa el mismo puerto 8080: no
> levantarlo a la vez que el compartido. Le falta el plugin `docker-workflow`, igual que al
> compartido; por eso el `Jenkinsfile` no usa `agent { docker ... }`.

## Protección de la base de producción (Neon)

El deploy **no puede** conectarse a Neon, y hay tres barreras:

1. `docker-compose.deploy.yml` fija `DATABASE_URL` al Postgres del propio compose. Es un literal:
   no se interpola desde el entorno ni desde `.env`.
2. El stage **Proteger DB de producción** aborta si alguna variable del build contiene `neon.tech`,
   o si el compose dejó de fijar la DB local. Solo imprime el nombre de la variable.
3. El **Smoke test** verifica, dentro del contenedor, que Django esté usando `HOST=db`.

**No crear una credencial `database-url`.** Versiones anteriores de esta guía lo sugerían ("o la
de Neon"), y como la API corre `migrate` al arrancar, eso habría aplicado migraciones sobre
producción desde un pipeline de demostración.

## Stages

| Stage | Qué verifica |
|---|---|
| Proteger DB de producción | Ninguna URL de Neon en el entorno; DB local fija en el compose |
| Test (gate) | `mypy` + `pytest` en un `python:3.12-slim` efímero. El código entra por `tar` por stdin, porque el workspace vive en el volumen de Jenkins y no en el host |
| Build image | `ghcr.io/nicolasandrescl/portafolio-backend:<commit>` y `:latest` |
| Push GHCR | Solo con `PUBLISH_GHCR=true`; requiere la credencial `ghcr-token` (usuario + PAT `write:packages`), que hoy no existe |
| Deploy | `docker compose -f docker-compose.deploy.yml up -d` con la imagen del commit |
| Healthcheck | `docker inspect` del contenedor `portafolio-deploy-api-1`; **falla** si queda `unhealthy` o no llega a `healthy` en 90 s |
| Smoke test | `/healthz/`, `/cv/`, `/cv/en/` y `/` con el `Content-Type` esperado |

¿Por qué `docker exec`/`inspect` y no `curl localhost:8001`? Desde el contenedor de Jenkins,
`localhost` es Jenkins mismo. ¿Por qué `docker` y no `docker compose` tras el deploy? Cualquier
`docker compose ...` vuelve a leer el archivo, y este exige `SECRET_KEY`, que solo existe dentro
del stage Deploy.

## Uso

- **Build Now** en `portafolio-cd` (o esperar al `pollSCM`, cada ~3 min).
- Resultado: http://localhost:8001

```bash
docker compose -f docker-compose.deploy.yml ps                        # api + db healthy
docker compose -p portafolio-deploy down                              # bajar el stack (conserva el volumen)
```
