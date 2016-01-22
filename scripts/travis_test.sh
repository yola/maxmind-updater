#!/bin/sh
# This script requires that $LICENSE_KEY is available in the environment
# (which Travis provides)

set -eux

db_file=geoip.mmdb
set +x
python -m maxmindupdater $db_file $LICENSE_KEY GeoIP2-Country
set -x

# Ensure file was produced
ls $db_file
