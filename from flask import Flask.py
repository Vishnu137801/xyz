version: "3.4"

services:
  redis:
    env_file:
      - ".env"
    image: "redis:5.0.4-stretch"
    restart: "${DOCKER_RESTART_POLICY:-unless-stopped}"
    stop_grace_period: "${DOCKER_STOP_GRACE_PERIOD:-3s}"
    volumes:
      - "redis:/data"

  web:
    build:
      context: "."
      args:
        - "FLASK_ENV=${FLASK_ENV:-production}"
    depends_on:
      - "redis"
    env_file:
      - ".env"
healthcheck:
      test: "${DOCKER_HEALTHCHECK_TEST:-curl localhost:8000/healthy}"
      interval: "60s"
      timeout: "3s"
      start_period: "5s"
      retries: 3
    ports:
      - "${DOCKER_WEB_PORT:-127.0.0.1:8000}:8000"
    restart: "${DOCKER_RESTART_POLICY:-unless-stopped}"
    stop_grace_period: "${DOCKER_STOP_GRACE_PERIOD:-3s}"
    volumes:
      - "${DOCKER_WEB_VOLUME:-./public:/app/public}"

  worker:
    build:
      context: "."
      args:
        - "FLASK_ENV=${FLASK_ENV:-production}"
    command: celery worker -B -l info -A snakeeyes.blueprints.contact.tasks
    depends_on:
      - "redis"
    env_file:
      - ".env"
    restart: "${DOCKER_RESTART_POLICY:-unless-stopped}"
    stop_grace_period: "${DOCKER_STOP_GRACE_PERIOD:-3s}"
    volumes:
      - "${DOCKER_WEB_VOLUME:-./public:/app/public}"

volumes:
  redis: {}