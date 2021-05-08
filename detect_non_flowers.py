#!/usr/bin/env python
import web
import sys, os, re, shutil
import json
from pydal import DAL
sys.path.append('.')
from model import define_tables
db = DAL('sqlite://flower_storage.db', folder='./data')

OPTION_INIT = 1
OPTION_FP = 2
OPTION_FN = 3

start_from = 0
num_images = 50

run_option = OPTION_INIT


urls = (
    '/', 'home',
    '/get_images', 'get_images',
    '/update_image_data', 'update_image_data'
)

app = web.application(urls, globals())

define_tables(db)

def get_images_query(start_from, num_images, run_option):
    base_query = (db.images.is_live == True) & (db.images.is_non_flower == None)
    print (run_option)
    if run_option == OPTION_FP:
        base_query = (
            (db.images.is_non_flower_model_prediction == True) &
            (db.images.is_non_flower == False) &
            (db.images.is_live == True)
        )
    elif run_option == OPTION_FN:
        base_query = (
            (db.images.is_non_flower_model_prediction == False) &
            (db.images.is_non_flower == True) &
            (db.images.is_live == True)
        )

    return db(base_query).select(db.images.id, db.images.url, db.images.is_non_flower,
        limitby=(start_from, start_from + num_images))

class home:
    def GET(self):
        with open('detect_non_flowers_templates/home.html') as f:
            main_template = f.read()
        return main_template

class get_images:
    def GET(self):
        global run_option
        web.header('Content-Type', 'text/json')
        images = get_images_query(start_from, num_images, run_option)
        return json.dumps({'images': images.as_list()})

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

if __name__ == "__main__":
#     while True:
#         run_option = input(
# """Select run mode
# 1. Initial - all not downloaded files
# 2. False Positives - find files marked as non flowers but are closeup flowers
# 3. False Negatives - find files not marked as non flowers but are not closeup flowers
# """
#         )
#         if run_option not in ('1', '2', '3'):
#             print ("No such option")
#         else:
#             break

    app.run()
