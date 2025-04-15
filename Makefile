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

include deployed-environments.env
export

.PHONY: replace-test-env-rds-state-with-prod-copy
replace-test-env-rds-state-with-prod-copy:
	kubectl run psql \
	--image=postgres:13.16 \
	--namespace journal--test \
	--env=PGHOST=$(PGHOST) \
	--env=PGDATABASE=$(PGDATABASE) \
	--env=PGUSER=$(PGUSER) \
	--env=PGPASSWORD=$(PGPASSWORD) \
	-- sleep 600
	kubectl wait --namespace journal--test --for condition=Ready pod psql
	kubectl exec --namespace journal--test psql -- psql -A -t -c "COPY digests_digest TO STDOUT WITH (FORMAT CSV, HEADER);" > digests_digest.csv
	kubectl delete --namespace journal--test pod psql
	kubectl run psql \
	--image=postgres:13.16 \
	--namespace journal--test \
	--overrides='{"spec": {"containers":[{"name": "psql", "image": "postgres:13.16", "args": ["sleep", "600"], "envFrom":[{ "secretRef": { "name": "digests-database-secret" } }]}]}}'

	echo drop all test env tables
	echo apply prod dump to test RDS
