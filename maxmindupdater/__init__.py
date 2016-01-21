"""Function to keep a maxmind database file up to date"""

import hashlib
import os
import shutil
import sys
import tarfile

import requests

__version__ = '0.1.0'
__url__ = 'https://github.com/yola/maxmind-updater'

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


def update_db(db_path, license_key, edition_id):
    db_dir_path = os.path.dirname(db_path)

    def maxmind_download(suffix, **kwargs):
        return requests.get(UPDATE_URL,
                            params={'license_key': license_key,
                                    'edition_id': edition_id,
                                    'suffix': suffix,
                                    },
                            **kwargs)

    expected_md5 = maxmind_download('tar.gz.md5').content
    curr_md5 = hash_file('%s.tar.gz' % db_path)
    if expected_md5 == curr_md5 and os.path.exists(db_path):
        return

    with open('%s.tar.gz' % db_path, 'wb') as local_zip:
        for chunk in maxmind_download('tar.gz', stream=True
                                      ).iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                local_zip.write(chunk)

    with tarfile.open('%s.tar.gz' % db_path) as tar_file:
        # We only want the mmdb file. Maxmind kindly includes things
        # we don't want.
        extract_members = [member for member in tar_file.getmembers()
                           if member.name.endswith('.mmdb')]
        tar_file.extractall(path=db_dir_path, members=extract_members)
        # extractall keeps the subfolder structure. Account for this by
        # appending the path to the db_dir_path where it was extracted.
        new_db = os.path.join(db_dir_path, extract_members[0].path)
    try:
        pass
        # TODO
        # test_ip('8.8.8.8', new_db)
        # test_ip('2001:420::', new_db)
    except Exception, e:
        # pyGeoIP could break in a variety of ways - we don't
        # particularly care which ones.
        sys.stderr.write('Retrieved invalid GeoIP database - '
                         'check MaxMind account details: %s' % e)
    else:
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        shutil.move(new_db, db_path)
        os.rmdir(os.path.dirname(new_db))
