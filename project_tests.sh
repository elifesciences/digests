#!/bin/bash
set -e

cd src/
pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml

