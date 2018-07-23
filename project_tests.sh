#!/bin/bash
set -e

pipenv install --dev

cd src/

pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml

