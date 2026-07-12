// Pipeline de CD del portafolio backend.
// CI (tests en cada push/PR) vive en GitHub Actions; este pipeline hace CD:
// gate de tests -> build de imagen -> push a GHCR -> deploy con docker compose.
pipeline {
    agent any

    // Jenkins local no recibe webhooks de GitHub: poll cada ~3 min.
    // (En servidor / con túnel, reemplazar por trigger por webhook.)
    triggers {
        pollSCM('H/3 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        REGISTRY = 'ghcr.io'
        IMAGE    = 'ghcr.io/nicolasandrescl/portafolio-backend'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test (gate)') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    python -m pip install --no-cache-dir -r requirements-dev.txt
                    mypy portfolio_app portfolio_project
                    pytest
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE:${GIT_COMMIT} -t $IMAGE:latest .'
            }
        }

        stage('Push GHCR') {
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
                withCredentials([
                    string(credentialsId: 'django-secret-key', variable: 'SECRET_KEY'),
                    string(credentialsId: 'database-url', variable: 'DATABASE_URL')]) {
                    sh '''
                        export SECRET_KEY DATABASE_URL
                        docker compose -f docker-compose.deploy.yml pull api
                        docker compose -f docker-compose.deploy.yml up -d
                        # Espera a que el api quede healthy
                        for i in $(seq 1 15); do
                            if curl -fsS http://localhost:8000/healthz/ >/dev/null; then
                                echo "healthz OK"; break
                            fi
                            echo "esperando healthz ($i)..."; sleep 4
                        done
                        docker compose -f docker-compose.deploy.yml ps
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
        success {
            echo 'CD OK: imagen publicada en GHCR y stack desplegado.'
        }
        failure {
            echo 'CD falló: revisar el stage que quedó en rojo.'
        }
    }
}
