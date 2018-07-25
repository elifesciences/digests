#!/usr/bin/env bash

source venv/bin/activate

until echo > /dev/tcp/db/5432; do sleep 1; done

python app/manage.py migrate
