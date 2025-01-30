ARG python_version
ARG image_tag=latest
FROM elifesciences/python_3.8:${python_version} AS venv

ARG pipenv_dev_arg

# lsh@2022-07-27: uwsgi needs to be built, uncertain how it was happening before.
# note: 'python3-dev' under 'elifesciences/python_3.8' will install python3.9-dev and python3.9.
#       - https://packages.debian.org/bullseye/python3-dev
USER root
RUN apt-get update -y && \
    apt-get install build-essential python3-dev clang git -y --no-install-recommends

ENV PROJECT_FOLDER=/srv/digests
WORKDIR ${PROJECT_FOLDER}

RUN python3.8 -m venv venv
ENV VIRTUAL_ENV=${PROJECT_FOLDER}/venv

COPY Pipfile Pipfile.lock ./
RUN pipenv install ${pipenv_dev_arg} --deploy


FROM elifesciences/python_3.8:${python_version} AS digests

ENV PROJECT_FOLDER=/srv/digests
WORKDIR ${PROJECT_FOLDER}

USER root
RUN mkdir -p var/logs && \
    chown --recursive elife:elife . && \
    chown www-data:www-data var/logs

RUN apt-get update -y && \
    apt-get install curl -y --no-install-recommends

COPY --chown=elife:elife smoke_tests_wsgi.sh .
COPY --chown=elife:elife migrate.sh .
COPY --from=venv --chown=elife:elife ${PROJECT_FOLDER}/venv/ venv/
COPY --chown=elife:elife app/ app/

USER www-data
CMD ["venv/bin/python"]
HEALTHCHECK --interval=5s CMD bash -c "venv/bin/uwsgi_curl 127.0.0.1:9000 localhost/ping | grep pong"

FROM elifesciences/python_3.8:${python_version} AS ci

ENV PROJECT_FOLDER=/srv/digests
WORKDIR ${PROJECT_FOLDER}

USER root
RUN mkdir -p /var/www build && \
    chown www-data:www-data /var/www build && \
    mkdir -p var/logs && \
    chown www-data:www-data var/logs

COPY --from=venv ${PROJECT_FOLDER}/venv/ venv/
COPY project_tests.sh Pipfile Pipfile.lock ./
COPY --from=digests ${PROJECT_FOLDER}/app/ app/

USER www-data
CMD ["./project_tests.sh"]
