#!/bin/bash
set -e

source venv/bin/activate
pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml
