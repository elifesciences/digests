#!/usr/bin/env bash
set -ex

source venv/bin/activate

until echo > /dev/tcp/localhost/9000; do sleep 1; done

uwsgi_curl 127.0.0.1:9000 "localhost/ping"
uwsgi_curl 127.0.0.1:9000 "localhost/digests"
