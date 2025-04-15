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
	kubectl exec --namespace journal--test psql -- psql -c "TRUNCATE digests_digest"
	kubectl cp --namespace journal--test ./digests_digest.csv psql:/digests_digest.csv
	kubectl exec --namespace journal--test psql -- psql -c "\copy digests_digest FROM '/digests_digest.csv' WITH CSV HEADER"
	kubectl delete --namespace journal--test pod psql


.PHONY: replace-prod-env-rds-state-with-prod-copy
replace-prod-env-rds-state-with-prod-copy:
	kubectl run psql \
	--image=postgres:13.16 \
	--namespace journal--prod \
	--env=PGHOST=$(PGHOST) \
	--env=PGDATABASE=$(PGDATABASE) \
	--env=PGUSER=$(PGUSER) \
	--env=PGPASSWORD=$(PGPASSWORD) \
	-- sleep 600
	kubectl wait --namespace journal--prod --for condition=Ready pod psql
	kubectl exec --namespace journal--prod psql -- psql -A -t -c "COPY digests_digest TO STDOUT WITH (FORMAT CSV, HEADER);" > digests_digest.csv
	kubectl delete --namespace journal--prod pod psql

	kubectl run psql \
	--image=postgres:13.16 \
	--namespace journal--prod \
	--overrides='{"spec": {"containers":[{"name": "psql", "image": "postgres:13.16", "args": ["sleep", "600"], "envFrom":[{ "secretRef": { "name": "digests-database-secret" } }]}]}}'
	kubectl exec --namespace journal--prod psql -- psql -c "TRUNCATE digests_digest"
	kubectl cp --namespace journal--prod ./digests_digest.csv psql:/digests_digest.csv
	kubectl exec --namespace journal--prod psql -- psql -c "\copy digests_digest FROM '/digests_digest.csv' WITH CSV HEADER"
	kubectl delete --namespace journal--prod pod psql
