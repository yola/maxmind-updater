#!/usr/bin/env bash

set -eux

python_version=$(python --version 2>&1 | cut -d ' ' -f2)
db_file=geoip_${python_version}.mmdb
PYTHONPATH=`pwd`
python maxmindupdater/__main__.py $db_file $LICENSE_KEY GeoIP2-Country

# Ensure all python versions produce the same result (and that they actually produced a result)
for other_db_file in geoip_*.mmdb ; do
    cmp $db_file $other_db_file
done
