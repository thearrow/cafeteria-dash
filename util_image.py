import config
import os
from PIL import Image
import numpy
import time


def process(image):
    image = image.convert('L')                                                  # grayscale
    image = image.resize((config.IMG_W, config.IMG_H), Image.LANCZOS)           # resize
    return image


def load(filename):
    if os.path.isfile(filename):
        return Image.open(filename)
    else:
        print "Error finding image file {}".format(filename)
        return null


def save(image):
    filename = "%(time)d.jpg" % {"time": time.time()}                           # seconds since epoch
    image.save(filename)


def save(image, filename):
    image.save(filename)


def data(image):
    return numpy.asarray(list(image.getdata()), numpy.float32) / 255.           # scale image data from [0, 255] to [0, 1]


def get_single_input_data(image):
    img = process(image)
    input = data(img)
    input = input.reshape(1, len(input))
    return input