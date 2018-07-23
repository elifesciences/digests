#!/bin/bash
set -e

pipenv install --dev

pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml

