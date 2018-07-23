#!/bin/bash
set -e

pipenv run proofreader --target core
pipenv run pytest --junitxml=build/pytest.xml

