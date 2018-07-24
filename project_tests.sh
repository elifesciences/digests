#!/bin/bash
set -e

source venv/bin/activate
cd app
pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml core.tests
