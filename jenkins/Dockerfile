# Jenkins LTS + Docker CLI + docker compose, para que el pipeline pueda
# construir imágenes y desplegar con docker compose usando el daemon del host.
FROM jenkins/jenkins:lts-jdk17

USER root

# Docker CLI + plugin compose (no el daemon: se usa el del host vía socket montado)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

USER jenkins

# Plugins base del pipeline (declarativo + docker + git/github + credenciales)
RUN jenkins-plugin-cli --plugins \
    workflow-aggregator \
    docker-workflow \
    git \
    github \
    credentials-binding \
    pipeline-stage-view
