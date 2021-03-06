ARG image_tag=latest
ARG python_version
FROM elifesciences/digests_venv:${image_tag} as venv
FROM elifesciences/python_3.6:${python_version}

ENV PROJECT_FOLDER=/srv/digests
WORKDIR ${PROJECT_FOLDER}

USER root
RUN mkdir -p var/logs && \
    chown --recursive elife:elife . && \
    chown www-data:www-data var/logs

COPY --chown=elife:elife smoke_tests_wsgi.sh .
COPY --chown=elife:elife migrate.sh .
COPY --from=venv --chown=elife:elife ${PROJECT_FOLDER}/venv/ venv/
COPY --chown=elife:elife app/ app/

USER www-data
CMD ["venv/bin/python"]
HEALTHCHECK --interval=5s CMD bash -c "venv/bin/uwsgi_curl 127.0.0.1:9000 localhost/ping | grep pong"
