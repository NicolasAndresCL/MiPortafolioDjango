# Workflows desactivados

GitHub Actions solo ejecuta lo que está en `.github/workflows/`. Estos quedan aquí como
**referencia**, sin ejecutarse:

- `build.yml` — build y push de la imagen a GHCR. **Lo reemplaza el CD en Jenkins** (`Jenkinsfile`).
- `deploy.yml` — deploy a PythonAnywhere por SSH. Reemplazado por el CD con docker compose de
  Jenkins. (El deploy a PythonAnywhere puede seguir haciéndose manual si se quiere.)

Reparto actual: **GitHub Actions = CI** (`ci.yml`, tests) · **Jenkins = CD** (ver `jenkins/`).
Para reactivar alguno, moverlo de vuelta a `.github/workflows/`.
