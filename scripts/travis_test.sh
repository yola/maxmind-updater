#!/bin/sh

set -eux

db_file=geoip.mmdb
set +x
python -m maxmindupdater $db_file $LICENSE_KEY GeoIP2-Country
set -x

# Ensure file was produced
ls $db_file
