#!/usr/bin/make -f

DOCKER_COMPOSE = docker compose -f docker-compose.yml

.PHONY: test
test: ci-test

.PHONY: start
start:
	$(DOCKER_COMPOSE) up --wait
	@echo Server running: http://localhost:8080/digests

.PHONY: stop
stop:
	$(DOCKER_COMPOSE) down -v

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs

.PHONY: ci-test
ci-test:
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml up --build -d
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml exec wsgi bash project_tests.sh
	$(DOCKER_COMPOSE) down

.PHONY: ci-smoketest
ci-smoketest:
	$(DOCKER_COMPOSE) up --build --wait -d
	$(DOCKER_COMPOSE) exec wsgi bash ./smoke_tests_wsgi.sh
	$(DOCKER_COMPOSE) down
