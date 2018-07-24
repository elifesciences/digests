#!/usr/bin/env bash
set -ex

source venv/bin/activate

uwsgi_curl 127.0.0.1:9000 "localhost/ping"
#uwsgi_curl 127.0.0.1:9000 "localhost/digests"
