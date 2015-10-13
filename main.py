import config
import util_image
import util_guru
import trainer
import numpy as np
import theanets
import glob


np.set_printoptions(precision=3)

mode = raw_input("1: Train\n2: Load\n3: Live\n")
exp = theanets.Experiment(
        theanets.feedforward.Regressor,
        layers=(config.IMG_W * config.IMG_H, 500, 1)
        )

if mode == "1":
    trainer.train(exp)

if mode == "2":
    exp = exp.load(path="net.data")
    print "Manual validation:"
    for file in glob.glob("data/manual/*.jpg"):
        image = util_image.load(file)
        input = util_image.data(image)
        input = input.reshape(1, len(input))
        output = exp.predict(input)
        print "Prediction for ", file, " = ", output

if mode == "3":
    exp = exp.load(path="net.data")
    session = util_guru.start()
    while True:
        image = util_guru.download(session)
        print "Opening image..."
        image.show()
        input = util_image.get_single_input_data(image)
        output = exp.predict(input)[0][0]
        print "Crowded Level: ", output
        raw_input("Any key to download another image...")
