import config
import util_image
import glob
import numpy as np


def build():                                               
    data = []

    for file in glob.glob("data/*.jpg"):
        output = file.split("-")[1].split('.')[0]                   # filename is {time}-{target}.jpg
        image = util_image.load(file)
        input = util_image.data(image)
        print "Adding sample: ", input, " => ", output
        data.append([input, output])

    final = np.array(data)
    np.random.shuffle(final)
    return final


def split(data, percent):                                           # training split (eg .85 for 85% of data used for training)
    index = len(data) * percent
    training = (np.vstack(data[:index,0]), np.array(data[:index,1], np.float32))
    validation = (np.vstack(data[index:,0]), np.array(data[index:,1], np.float32))

    training = (training[0].reshape(len(training[0]), -1).astype('f'), training[1].reshape(len(training[1]), -1).astype('f'))
    validation = (validation[0].reshape(len(validation[0]), -1).astype('f'), validation[1].reshape(len(validation[1]), -1).astype('f'))

    return (training, validation)