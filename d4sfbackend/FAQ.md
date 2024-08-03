
## FAQs!

* DeadlineExceeded: python:3.8: failed to authorize:
https://stackoverflow.com/questions/65601592/building-docker-image-fails-with-failed-to-fetch-anonymous-token-tls-handshake
Add line this file .bashrc:

```bash
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0
```

* Run/Debug configuration in IDE Pycharm

```bash
Working directory: /home/dlopez/PycharmProjects/d4sf/d4sfbackend
Environment variables: DJANGO_SETTINGS_MODULE=backend.settings.dev;PYTHONPATH=/d4sfbackend;PYTHONUNBUFFERED=1
Paths to ".env" files: /home/dlopez/PycharmProjects/d4sf/d4sfbackend/devops/local/.env
```