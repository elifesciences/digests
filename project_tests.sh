#!/bin/bash
set -e

source venv/bin/activate
cd app

until echo > /dev/tcp/db/5432; do sleep 1; done

pipenv run pytest --junitxml=../build/pytest.xml
