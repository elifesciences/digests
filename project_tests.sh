#!/bin/bash
set -e

source venv/bin/activate
cd app

# pytest can run specific tests with "-k <testname>"
# for example: "pytest -k test_returns_400_for_invalid_content_data"
args="$@"
if [ ! -z "$args" ]; then
    module="-k $args"
fi

proofreader --target core
DATABASE_URL=postgres://root:root@localhost:5432/digests pytest --junitxml=../build/pytest.xml $module
