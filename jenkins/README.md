# Jenkins (CD) — Portafolio backend

Servidor Jenkins containerizado que ejecuta el pipeline de **CD** (`Jenkinsfile` en la raíz del
backend): gate de tests → build de imagen → push a GHCR → deploy con `docker-compose.deploy.yml`.

El **CI** (tests en cada push/PR) vive en GitHub Actions (`.github/workflows/ci.yml`). Jenkins
se ocupa del **CD**.

## 1. Levantar Jenkins

```bash
docker compose -f jenkins/docker-compose.yml up -d --build
```

- UI: http://localhost:8080
- Contraseña inicial:
  ```bash
  docker exec portafolio-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```
- Completar el asistente (instalar plugins sugeridos; los específicos ya vienen en la imagen).

## 2. Verificar acceso a Docker (socket del host)

```bash
docker exec portafolio-jenkins docker version
docker exec portafolio-jenkins docker compose version
```

## 3. Credenciales (Manage Jenkins → Credentials → System → Global)

| ID | Tipo | Valor |
|---|---|---|
| `ghcr-token` | Username with password | usuario GitHub + **PAT** con scope `write:packages` |
| `django-secret-key` | Secret text | una `SECRET_KEY` fuerte (≥32 chars) |
| `database-url` | Secret text | `postgres://portafolio:portafolio@db:5432/portafolio` (Postgres del compose) o la de Neon |

## 4. Crear el pipeline

New Item → **Pipeline** → *Pipeline script from SCM* → Git → URL del repo, rama `main`,
Script Path `Jenkinsfile`. Guardar y **Build Now**.

El pipeline corre los 5 stages; al terminar, el stack queda desplegado:

```bash
docker compose -f docker-compose.deploy.yml ps      # api + db healthy
curl http://localhost:8000/healthz/                 # {"status": "ok"}
```

## Triggers

Jenkins local no recibe webhooks de GitHub, por eso el `Jenkinsfile` usa `pollSCM` (~cada 3 min).
Para disparo por evento:
- **Túnel** (local): exponer `:8080` con `cloudflared`/`ngrok` y configurar el webhook de GitHub.
- **Servidor**: mover Jenkins + el deploy a un host (p. ej. el EC2 de `terraform/`) y usar webhook
  directo; cambiar `DATABASE_URL` a Neon/RDS.

## Detener / limpiar

```bash
docker compose -f jenkins/docker-compose.yml down          # detener Jenkins (conserva jenkins_home)
docker compose -f docker-compose.deploy.yml down           # bajar el stack desplegado
```
