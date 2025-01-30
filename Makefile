#!/usr/bin/make -f

DOCKER_COMPOSE_DEV = docker-compose
DOCKER_COMPOSE_CI = docker-compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)

logs:
	mkdir -p logs && chmod a+w logs

build:
	$(DOCKER_COMPOSE) build

test: logs
	$(DOCKER_COMPOSE) run wsgi \
		venv/bin/pytest app/digests/tests/test_digest_api.py

start: logs
	$(DOCKER_COMPOSE) up -d web

clean:
	$(DOCKER_COMPOSE) down -v
