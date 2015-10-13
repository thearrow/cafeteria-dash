import numpy as np
import dataset
import theanets


def train(exp):
    data = dataset.build()
    training, validation = dataset.split(data, .80)

    print "Data loaded! Training..."
    exp.train(
        training,
        validation,
        optimize="nag",
        learning_rate=.0001,
        momentum=0.5
        )

    print "Saving network to net.data..."
    exp.save("net.data")