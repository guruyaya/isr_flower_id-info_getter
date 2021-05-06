img_dir = 'data/images_is_flower'
import os
import random
import re

numeric_dir_regex = re.compile("^\.[/\\\\][0-1]")
os.chdir(img_dir)

for dir_to_create in ('train', 'test', 'train/0', 'test/0', 'train/1', 'test/1'):
    if not os.path.isdir(dir_to_create): os.mkdir(dir_to_create)


for root, _, files in os.walk(".", topdown=False):
    for name in files:
        if (numeric_dir_regex.match(root)):
            file_to_move = os.path.join(root, name)
            target = 'train' if random.random() > 0.3 else 'test'
            os.rename(file_to_move, os.path.join(target, file_to_move))


