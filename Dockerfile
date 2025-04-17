ARG image_tag=latest

FROM ghcr.io/elifesciences/python:3.8 AS python-base

# lsh@2022-07-27: uwsgi needs to be built, uncertain how it was happening before.
# note: 'python3-dev' under 'elifesciences/python_3.8' will install python3.9-dev and python3.9.
#       - https://packages.debian.org/bullseye/python3-dev
USER root
RUN apt-get update -y && \
    apt-get install build-essential python3-dev clang git libpq-dev -y --no-install-recommends

ENV PROJECT_FOLDER=/srv/digests
WORKDIR ${PROJECT_FOLDER}

RUN python3.8 -m venv venv
ENV VIRTUAL_ENV=${PROJECT_FOLDER}/venv



FROM python-base AS prod-venv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy



FROM python-base AS dev-venv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --dev --deploy



FROM python-base AS dev
RUN mkdir -p var/logs && \
    chown --recursive elife:elife . && \
    chown www-data:www-data var/logs
COPY --chown=elife:elife smoke_tests_wsgi.sh .
COPY --chown=elife:elife migrate.sh .
COPY --from=dev-venv --chown=elife:elife ${PROJECT_FOLDER}/venv/ venv/
COPY --chown=elife:elife app/ app/
COPY project_tests.sh .



FROM python-base AS prod

RUN mkdir -p var/logs && \
    chown --recursive elife:elife . && \
    chown www-data:www-data var/logs

RUN apt-get update -y && \
    apt-get install curl -y --no-install-recommends

COPY --chown=elife:elife smoke_tests_wsgi.sh .
COPY --chown=elife:elife migrate.sh .
COPY --from=prod-venv --chown=elife:elife ${PROJECT_FOLDER}/venv/ venv/
COPY --chown=elife:elife app/ app/

USER www-data
CMD ["venv/bin/python"]
HEALTHCHECK --interval=5s CMD bash -c "venv/bin/uwsgi_curl 127.0.0.1:9000 localhost/ping | grep pong"
