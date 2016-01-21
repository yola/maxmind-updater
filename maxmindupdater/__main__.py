#!/usr/bin/env python
from argparse import ArgumentParser
from maxmindupdater import update_db


def main():
    parser = ArgumentParser()
    parser.add_argument('db_path')
    parser.add_argument('license_key')
    parser.add_argument('edition_id')
    args = parser.parse_args()
    update_db(args.db_path, args.license_key, args.edition_id)


if __name__ == '__main__':
    main()
