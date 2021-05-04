#!/usr/bin/env python
from urllib.request import urlopen, Request
import urllib

from pydal import DAL
import os, sys
import re
sys.path.append('.')
from model import define_tables


db = DAL('sqlite://flower_storage.db', folder='./data')
define_tables(db)

base_dir = 'data/images'

def mkdir(dir_name):
    if (not os.path.exists(dir_name)):
        os.mkdir(dir_name)

def get_file(url, dir_name, file_name, skip_count):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    full_path = '{}/{}'.format(dir_name, file_name)
    if (os.path.exists(full_path)):
        if skip_count % 300 == 0:
            print (".", end='')
        return skip_count+1

    print ("Downloading {}...".format(full_path))

    mkdir(dir_name)

    req = Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    with urlopen(req) as response, open(full_path, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)
    return skip_count

def main():
    skip_count = 0;
    ext_re = re.compile('\.([A-Za-z0-9]*)$')
    for image in db().select(db.images.ALL):
        ext = ext_re.findall(image.url)[0]
        dir_name = '{}/{}'.format(base_dir, image.flower_id)
        file_name = '{}.{}'.format(image.id, ext)
        try:
            skip_count = get_file(image.url, dir_name, file_name, skip_count)
        except urllib.error.URLError:
            print ("SSL ERR")
        except ConnectionResetError:
            print ("RESET ERR")

if __name__ == '__main__':
    main()
