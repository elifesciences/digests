# digests

## Install a new dev package

For consistency of environment, use the `venv` container:

```
docker-compose run venv pipenv install --dev uwsgi-tools
docker-compose run venv pipenv lock
```
