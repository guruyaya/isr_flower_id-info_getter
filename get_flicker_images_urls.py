#!/usr/bin/env python
import configparser
import flickr_api
from pydal import DAL
import sys
import sqlite3
sys.path.append('.')
from model import define_tables


config = configparser.ConfigParser()
config.read('config.ini')
flickr_api.set_keys(api_key = config['flicker']['key'],
                    api_secret = config['flicker']['secret'])

db = DAL('sqlite://flower_storage.db', folder='./data')
define_tables(db)

flowers = db().select(db.flowers.ALL)

for flower in flowers:
    print ("Flower name: {}".format(flower.name))
    num_flowers_left = int(config['flicker']['num_images']) - db(db.images.flower_id == flower.id).count()
    if num_flowers_left <= 0:
        print ("Skipping...")
        continue

    w = flickr_api.Walker(
            flickr_api.Photo.search, tags=flower.name
    )
    for i, photo in enumerate(w):
        try:
            db.images.insert(url=photo['url_m'], flower_id=flower.id)
            db.commit()
        except sqlite3.IntegrityError:
            print ("URL {} is in DB".format(photo['url_m']))
        except KeyError:
            try:
                db.images.insert(url=photo['url_n'], flower_id=flower.id)
            except sqlite3.IntegrityError:
                print ("URL {} is in DB".format(photo['url_n']))

        if i > num_flowers_left:
            break
