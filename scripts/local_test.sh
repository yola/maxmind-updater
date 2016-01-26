#!/bin/sh
# Used by Yola internally for testing (mainly to automatically obtain a license key)

set -eux

configurator --local userservice qa
license_key=$(python -c "print __import__('json').load(open('configuration.json'))['userservice']['geoip']['license_key']")
rm configuration.json

./virtualenv/bin/python maxmindupdater/__main__.py geoip.mmdb $license_key GeoIP2-Country
