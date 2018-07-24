#!/bin/bash
set -e

cd app
pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml

