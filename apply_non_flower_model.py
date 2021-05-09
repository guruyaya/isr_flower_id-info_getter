import tensorflow as tf
import numpy as np
import re
import pandas as pd
from glob import glob
from tensorflow import keras
from tensorflow.keras import layers
from PIL import UnidentifiedImageError
from PIL.Image import DecompressionBombError
from model import define_tables
from pydal import DAL

data_dir = 'data/images'

img_height = 224
img_width = 224
image_size = (img_width, img_height)

base_model = tf.keras.applications.MobileNetV3Large(input_shape=(img_height, img_width, 3),
                                               include_top=False,
                                               weights='imagenet')
base_model.trainable = False

preprocess_input = tf.keras.applications.mobilenet_v3.preprocess_input
prediction_layer = tf.keras.layers.Dense(1, activation='sigmoid')
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()

inputs = tf.keras.Input(shape=(img_width, img_height, 3))
x = preprocess_input(inputs)
x = base_model(x, training=False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['binary_accuracy'])

model.load_weights('data/model_is_flower.json')

image_id_re = re.compile(".*[/\\\\]([0-9]+)\.[A-Za-z0-9]+")
img_filenames = glob(data_dir + '/*/*')
num_images = len(img_filenames)
images = []
image_ids = []
scores = pd.Series([], dtype='float64')

def handle_predictions_batch(n, images, model, scores):
    print (f"handling image number {n} / {num_images}: {image}")
    images = np.vstack(images)
    predictions = model.predict(images)
    partial_scores = pd.Series(predictions[:, 0], index=image_ids)
    return pd.concat([scores, partial_scores])

for n, image in enumerate(img_filenames, 1):
    if (n) % 1000 == 0:
        scores = handle_predictions_batch(n, images, model, scores)
        # Clear images batch
        image_ids = []
        images = []

    try:
        img = keras.preprocessing.image.load_img(
            image, target_size=image_size
        )
    except UnidentifiedImageError as e:
        print (f"UnidentifiedImage, Skipping image {image} (#{n})")
    except DecompressionBombError as e:
        print (f"DecompressionBomb, Skipping image {image} (#{n})")
    else:
        image_ids.append(int( image_id_re.match(image)[1] ))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        images.append(img_array)

scores = handle_predictions_batch(n, images, model, scores)

db = DAL('sqlite://flower_storage.db', folder='./data')
define_tables (db)

db(db.images.id > 0).update(is_live=False)

db.commit()

is_non_flower_indexes = scores[scores > 0.5].index
db.executesql(
    "UPDATE images SET is_live='T', is_non_flower='T' WHERE id IN({})".format(
        ','.join( list(is_non_flower_indexes.astype('str')) )
    )
)
db.commit()

is_flower_indexes = scores[scores <= 0.5].index
db.executesql(
    "UPDATE images SET is_live='T', is_non_flower='F' WHERE id IN({})".format(
        ','.join( list(is_flower_indexes.astype('str')) )
    )
)
db.commit()

# %%
','.join(['1','2','3'])