import os
from pydal import DAL
from glob import glob
from model import define_tables
import random

def mkdir_if_not_exist(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

images_data_dir = 'data/images'
train_images_dir = 'data/train_images'
test_images_dir = 'data/test_images'
mkdir_if_not_exist(train_images_dir)
mkdir_if_not_exist(test_images_dir)

db = DAL('sqlite://flower_storage.db', folder='./data')
define_tables(db)

images_data = db((db.images.is_live == True) & 
        (db.images.is_non_flower == False)).select()

random.seed(42)
for image in images_data:
    filename_glob = images_data_dir + '/' + str(image.flower_id) + '/' + str(image.id) + '.*'
    try:
        filename = glob(filename_glob)[0]
    except KeyError:
        continue

    target = train_images_dir
    if random.random() > 0.7:
        target = test_images_dir

    target_filename = filename.replace(images_data_dir, target)
    target_dirname = os.path.dirname(target_filename)
    mkdir_if_not_exist(target_dirname)
    os.rename (filename, target_filename)
