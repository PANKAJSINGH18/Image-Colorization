import sys

import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

img_size = 128
fileurl = sys.argv[1]
filename = sys.argv[2]


def Load(image):
    image = tf.io.decode_jpeg(image, channels=1)
    image = tf.cast(image, tf.float32)
    return image

def GrayScale(image):
    image = tf.image.rgb_to_grayscale(image)
    return image

def resize(image, height, width):
    input_image = tf.image.resize(image, [height, width], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    return input_image

@tf.function
def jitter(real_image, height, width):
    real_image = resize(real_image, height, width)
    return real_image

def normalize( real_image):
    real_image = (real_image / 255)
    return real_image

def Load_image(image):
    real_image = Load(image)
    real_image = jitter(real_image, img_size, img_size)
    real_image = normalize(real_image)
    return  real_image

generator = tf.keras.models.load_model('Generator_Model')

image = tf.io.read_file(fileurl)
image = Load_image(image)
rgb_image = generator(image[tf.newaxis, ...], training=False)
rgb_image = rgb_image * 255
rgb_image = tf.cast(rgb_image, tf.uint8)
image_save_path = fileurl.replace(filename, "temp.png")
plt.imsave(str(image_save_path), np.array(rgb_image[0]))
print('/media/uploads/temp.png')

