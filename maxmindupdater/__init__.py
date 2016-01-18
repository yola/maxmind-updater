from shutil import move
import os
import hashlib
import sys
import tarfile

import requests

from userservice.lib.util import ip_to_country_code

UPDATE_URL = 'https://download.maxmind.com/app/geoip_download'


def hash_file(filename):
    if not os.path.exists(filename):
        return ''

    block_size = 65536
    hasher = hashlib.md5()

    with open(filename, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()


def update_db(curr_db, license_key):
        curr_db_path = os.path.dirname(curr_db)

        r = requests.get(UPDATE_URL,
                         params={'license_key': license_key,
                                 'edition_id': 'GeoIP2-Country',
                                 'suffix': 'tar.gz.md5',
                                 })

        curr_md5 = hash_file('%s.tar.gz' % curr_db)
        if r.content == curr_md5 and os.path.exists(curr_db):
            return

        r = requests.get(UPDATE_URL, stream=True,
                         params={'license_key': license_key,
                                 'edition_id': 'GeoIP2-Country',
                                 'suffix': 'tar.gz',
                                 })

        with open('%s.tar.gz' % curr_db, 'wb') as local_zip:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    local_zip.write(chunk)

        with tarfile.open('%s.tar.gz' % curr_db) as tar_file:
            # We only want the mmdb file. Maxmind kindly includes things
            # we don't want.
            extract_members = [member for member in tar_file.getmembers()
                               if member.name.endswith('.mmdb')]
            tar_file.extractall(path=curr_db_path, members=extract_members)
            # extractall keeps the subfolder structure. Account for this by
            # appending the path to the curr_db_path where it was extracted.
            new_db = os.path.join(curr_db_path, extract_members[0].path)
        try:
            ip_to_country_code('8.8.8.8', new_db)
            ip_to_country_code('2001:420::', new_db)
        except Exception, e:
            # pyGeoIP could break in a variety of ways - we don't
            # particularly care which ones.
            sys.stderr.write('Retrieved invalid GeoIP database - '
                             'check MaxMind account details: %s' % e)
        else:
            if not os.path.exists(os.path.dirname(curr_db)):
                os.makedirs(os.path.dirname(curr_db))
            move(new_db, curr_db)
            os.rmdir(os.path.dirname(new_db))