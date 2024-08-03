#!/bin/bash

# Uso: ./launch.sh entorno
# entorno: dev, prod, test

function pause_launch() {
  read -p "Press any key to continue. " -n1 -s
}

function check_install_docker_compose() {
    if $(docker-compose --version &>/dev/null) && [ $? -eq 0 ]; then
      echo "SUCCESS: docker-compose (v1) is installed."
    else
        sudo apt install docker-compose
    fi

    if $(docker compose &>/dev/null) && [ $? -eq 0 ]; then
      echo "SUCCESS: docker compose (v2) is installed."
    else
        echo "ERROR: neither \"docker-compose\" nor \"docker compose\" appear to be installed."
        exit 1
    fi
}

if [ "$#" -ne 1 ]; then
  echo "Uso: $0 entorno=[local/dev/test/prod]"
  exit 1
fi

ENTORNO=$1

case "$ENTORNO" in
  local)
    DOCKER_COMPOSE_FILE='docker-compose.yaml'
    ENVIRONMENT_FILE='devops/local/.env'
    ENVIRONMENT=dev
    ;;
  dev|development)
    DOCKER_COMPOSE_FILE='docker-compose.yaml'
    ENVIRONMENT_FILE='devops/dev/.env.dev'
    ENVIRONMENT=dev
    ;;
  prod|production)
    DOCKER_COMPOSE_FILE='devops/prod/docker-compose.yaml'
    ENVIRONMENT_FILE='devops/prod/.env.prod'
    ENVIRONMENT=prod
    ;;
  test|testing)
    DOCKER_COMPOSE_FILE='devops/test/docker-compose.yaml'
    ENVIRONMENT_FILE='devops/test/.env.test'
    ENVIRONMENT=test
    ;;
  *)
    echo "Entorno no válido. Usar 'development', 'testing' o 'production'."
    exit 1
    ;;
esac


check_install_docker_compose

docker-compose -f $DOCKER_COMPOSE_FILE --env-file $ENVIRONMENT_FILE config
sleep 3 &
#pause_launch

docker-compose -f $DOCKER_COMPOSE_FILE --env-file $ENVIRONMENT_FILE down
docker-compose -f $DOCKER_COMPOSE_FILE --env-file $ENVIRONMENT_FILE up --build -d