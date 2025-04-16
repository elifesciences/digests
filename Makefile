#!/usr/bin/make -f

DOCKER_COMPOSE_MULTISTAGE = docker compose -f docker-compose.multistage.yml

.PHONY: test
test: ci-test

.PHONY: start
start:
	$(DOCKER_COMPOSE_MULTISTAGE) -f docker-compose.prod.yml up --wait
	@echo Server running: http://localhost:8080/digests

.PHONY: stop
stop:
	$(DOCKER_COMPOSE_MULTISTAGE) down -v

.PHONY: logs
logs:
	$(DOCKER_COMPOSE_MULTISTAGE) logs

.PHONY: ci-test
ci-test:
	$(DOCKER_COMPOSE_MULTISTAGE) up --build -d
	$(DOCKER_COMPOSE_MULTISTAGE) exec wsgi bash project_tests.sh
	$(DOCKER_COMPOSE_MULTISTAGE) down

.PHONY: ci-smoketest
ci-smoketest:
	$(DOCKER_COMPOSE_MULTISTAGE) -f docker-compose.prod.yml up --build --wait -d
	$(DOCKER_COMPOSE_MULTISTAGE) exec wsgi bash ./smoke_tests_wsgi.sh
	$(DOCKER_COMPOSE_MULTISTAGE) down
