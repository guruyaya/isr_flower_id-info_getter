#!/usr/bin/env python
from selenium import webdriver
import time
import urllib.parse

import configparser
from pydal import DAL
import re
import sys
import sqlite3
sys.path.append('.')
from model import define_tables

config = configparser.ConfigParser()
config.read('config.ini')

db = DAL('sqlite://flower_storage.db', folder='./data')
define_tables(db)

def get_image_links(driver, search_term, count=50):
    re_links = re.compile('(https?://[^"]*\.(jpe?g|png|gif|webp))', re.I)
    gogole_link = "https://www.google.com/search?tbm=isch" +\
        "&source=hp" +\
        "&ei=2qO2XsevCseIlwSv25uIBQ" +\
        "&q=" + urllib.parse.quote(search_term) +\
        "&sclient=img"
    driver.get(gogole_link)
    source = driver.page_source
    links = re_links.findall(source)
    time.sleep(1)
    return ([link[0] for link in links])[:count]


def get_flowers_by_name(flowers, name_col='name'):
    try:
        driver = webdriver.Firefox()
        for flower in flowers:
            print ("Flower name: {}".format(flower.flowers[name_col]))
            flower_count = flower[ db.images.id.count() ]

            if flower_count >= max_flowers:
                print ("Skipping...")
                continue
            links = get_image_links(driver, flower.flowers[name_col], count=max_flowers-flower_count)
            for link in links:
                try:
                    db.images.insert(url=link, flower_id=flower.flowers.id)
                except sqlite3.IntegrityError:
                    print ("URL {} allready in db".format(link))
                db.commit()
    finally:
        time.sleep(5)
        driver.close()
        db.close()

max_flowers = int(config['google']['num_images'])



# Eng Names
flowers = db(db.flowers.eng_name != None).select(
    db.flowers.id, db.flowers.eng_name, db.images.id.count(),
                    groupby=db.images.flower_id,
                    left=db.images.on(db.images.flower_id == db.flowers.id),
                    having=(db.images.id.count() < 50)
)
get_flowers_by_name(flowers, 'eng_name')

# Hebrew Names
flowers = db().select(db.flowers.id, db.flowers.name, db.images.id.count(),
                    groupby=db.images.flower_id,
                    left=db.images.on(db.images.flower_id == db.flowers.id),
                    having=(db.images.id.count() < 50)
)
get_flowers_by_name(flowers, 'name')
