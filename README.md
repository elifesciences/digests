# digests

## Install a new dev package

For consistency of environment, use the `venv` container:

```
docker-compose run venv pipenv install --dev uwsgi-tools
docker-compose run venv pipenv lock
```

## Run a test

```
docker-compose build
docker-compose run wsgi venv/bin/pytest app/digests/tests/test_digest_api.py
```

Images currently have to be re-built for modifications to any part of the code to be noticed.
