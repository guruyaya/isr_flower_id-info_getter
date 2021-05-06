#!/usr/bin/env python
import web
import sys, os, re, shutil
import json
from pydal import DAL
sys.path.append('.')
from model import define_tables
db = DAL('sqlite://flower_storage.db', folder='./data')

urls = (
    '/', 'home',
    '/get_images', 'get_images',
    '/update_image_data', 'update_image_data'
)

app = web.application(urls, globals())

define_tables(db)

def get_images(start_from, num_images):
    return db(
        (db.images.is_live == True) & (db.images.is_non_flower == None)
    ).select(limitby=(start_from, start_from+num_images))

class home:
    def GET(self):
        with open('detect_non_flowers_templates/home.html') as f:
            main_template = f.read()
        return main_template
class get_images:
    def GET(self):
        web.header('Content-Type', 'text/json')
        images = db(
            (db.images.is_live == True) & (db.images.is_non_flower == None)
        ).select(db.images.id, db.images.url, limitby=(0, 50))
        return json.dumps({'images': images.as_list()})
if __name__ == "__main__":
    app.run()

class update_image_data:
    def POST(self):
        images_data = json.loads( web.data() )
        for image in images_data:
            db_img = db(db.images.id == image['id'])
            if image['target'] == 'non_flower':
                db_img.update(is_non_flower=True)
            if image['target'] == 'flower':
                db_img.update(is_non_flower=False)
            if image['target'] == 'not_loaded':
                db_img.update(is_live=False)

        db.commit()
        return "Great success"