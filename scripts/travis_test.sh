#!/usr/bin/env bash

set -eux

db_file=geoip.mmdb
export PYTHONPATH=`pwd`
set +x
python maxmindupdater/__main__.py $db_file $LICENSE_KEY GeoIP2-Country
set -x

# Ensure file was produced
ls $db_file
