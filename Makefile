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
