#!/bin/bash
set -e

python='python3.6'

if [ -z "$python" ]; then
    echo "$python not found, exiting"
    exit 1
fi

if [ ! -e "venv/bin/$python" ]; then
    echo "could not find venv/bin/$python, recreating venv"
    rm -rf venv
    $python -m venv venv
fi

source venv/bin/activate

if [ -e "requirements.txt.lock" ]; then
    # normal case
    pip install -r requirements.txt.lock
else
    # initial case
    pip install -r requirements.txt
    pip freeze > requirements.txt.lock
fi
