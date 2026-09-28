// Pipeline de CD del portafolio backend.
// CI (tests en cada push/PR) vive en GitHub Actions; este pipeline hace CD de un stack
// DEMOSTRATIVO local: gate de tests -> build de imagen -> [push a GHCR] -> deploy con
// docker compose -> healthcheck real + smoke test.
//
// Producción (PythonAnywhere + Neon) NO se toca desde aquí. El stack desplegado usa el
// Postgres de docker-compose.deploy.yml (DATABASE_URL fija ahí) y el stage "Proteger DB
// de producción" aborta si aparece una URL de Neon en el entorno del build.
//
// Controller: el Jenkins compartido de C:\dev\projects\jenkins (Docker, socket del host).
// Job y credencial se crean por código en su init.groovy.d (70-/71-portafolio-*.groovy).
pipeline {
    agent any

    // Jenkins local no recibe webhooks de GitHub: poll cada ~3 min.
    triggers {
        pollSCM('H/3 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    parameters {
        booleanParam(name: 'PUBLISH_GHCR', defaultValue: false,
            description: 'Publicar la imagen en GHCR (requiere la credencial ghcr-token: usuario + PAT con write:packages).')
    }

    environment {
        REGISTRY = 'ghcr.io'
        IMAGE    = 'ghcr.io/nicolasandrescl/portafolio-backend'
        COMPOSE  = 'docker compose -f docker-compose.deploy.yml'
        // Nombre fijo gracias a `name: portafolio-deploy` en el compose. Tras el deploy se usa
        // `docker` directo: cualquier `docker compose ...` re-lee el archivo y exige SECRET_KEY,
        // que solo existe dentro del withCredentials del stage Deploy.
        API_CTR  = 'portafolio-deploy-api-1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Proteger DB de producción') {
            steps {
                // Barrera explícita: ninguna variable del build puede traer la URL de Neon.
                // Se imprime solo el NOMBRE de la variable, nunca su valor.
                sh '''
                    hits=$(env | grep -i 'neon\\.tech' | cut -d= -f1 || true)
                    if [ -n "$hits" ]; then
                        echo "ABORTADO: variables con URL de Neon en el entorno: $hits"
                        exit 1
                    fi
                    grep -q 'DATABASE_URL: "postgres://portafolio:portafolio@db:5432/portafolio"' docker-compose.deploy.yml \
                        || { echo "ABORTADO: docker-compose.deploy.yml ya no fija la DB local."; exit 1; }
                    echo "OK: el deploy solo puede usar el Postgres local del compose."
                '''
            }
        }

        stage('Test (gate)') {
            steps {
                // Contenedor efímero python:3.12 (el mismo Python que el Dockerfile). El
                // código entra por stdin con tar: el workspace vive en el volumen de
                // Jenkins, no en el host, así que un `-v $WORKSPACE:...` montaría vacío.
                sh '''
                    tar -cf - --exclude=.git --exclude=env . | docker run --rm -i python:3.12-slim sh -ec '
                        mkdir /w && cd /w && tar -xf -
                        python -m pip install -q --no-cache-dir --root-user-action=ignore -r requirements-dev.txt
                        mypy portfolio_app portfolio_project
                        pytest -q
                    '
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE:${GIT_COMMIT} -t $IMAGE:latest .'
            }
        }

        stage('Push GHCR') {
            when { expression { params.PUBLISH_GHCR } }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'ghcr-token',
                    usernameVariable: 'GHCR_USER',
                    passwordVariable: 'GHCR_PAT')]) {
                    sh '''
                        echo "$GHCR_PAT" | docker login $REGISTRY -u "$GHCR_USER" --password-stdin
                        docker push $IMAGE:${GIT_COMMIT}
                        docker push $IMAGE:latest
                        docker logout $REGISTRY
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'portafolio-django-secret-key', variable: 'SECRET_KEY')]) {
                    // Despliega la imagen recién construida (tag = commit). Sin pull: vive
                    // en el mismo daemon Docker del host.
                    sh 'IMAGE_TAG=${GIT_COMMIT} $COMPOSE up -d'
                }
            }
        }

        stage('Healthcheck') {
            steps {
                // El estado de salud lo mide Docker dentro del contenedor. Desde Jenkins,
                // "localhost:8001" sería el propio contenedor de Jenkins, no la API.
                sh '''
                    for i in $(seq 1 30); do
                        s=$(docker inspect -f '{{.State.Health.Status}}' "$API_CTR")
                        [ "$s" = healthy ] && { echo "api healthy ($i)"; break; }
                        [ "$s" = unhealthy ] && { echo "api UNHEALTHY"; exit 1; }
                        sleep 3
                    done
                    [ "$s" = healthy ] || { echo "api no quedó healthy en 90 s (estado: $s)"; exit 1; }
                '''
            }
        }

        stage('Smoke test') {
            steps {
                // Rutas reales dentro del contenedor + qué base de datos está usando
                // (solo host y nombre, nunca credenciales).
                sh '''
                    docker exec -i "$API_CTR" python - <<'PY'
import urllib.request, sys
from django.conf import settings
import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings.production")
django.setup()
db = settings.DATABASES["default"]
print(f"DB en uso: {db['ENGINE'].rsplit('.', 1)[-1]} @ {db.get('HOST')}/{db.get('NAME')}")
if db.get("HOST") != "db" or "neon" in str(db.get("HOST")):
    sys.exit("ABORTADO: la API no está usando el Postgres local del compose.")
checks = [("/healthz/", "application/json"), ("/cv/", "application/pdf"),
          ("/cv/en/", "application/pdf"), ("/", "text/html")]
for path, ctype in checks:
    r = urllib.request.urlopen("http://localhost:8000" + path)
    got = r.headers.get("Content-Type", "")
    print(f"{path:10} {r.status} {got}")
    if r.status != 200 or not got.startswith(ctype):
        sys.exit(f"FALLO: {path} esperaba {ctype}")
PY
                '''
            }
        }
    }

    post {
        failure {
            echo 'CD falló: últimas líneas del api (si llegó a arrancar):'
            sh 'docker logs --tail 40 "$API_CTR" 2>&1 || true'
        }
        success {
            echo "CD OK: imagen ${env.GIT_COMMIT} desplegada en http://localhost:8001 (Postgres local)."
        }
        always {
            sh 'docker image prune -f || true'
        }
    }
}
