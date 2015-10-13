from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
import logging
import theanets
import util_guru


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
#app.debug = True
app.config.from_object('config')
app.config.from_object('config_weather')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

session = util_guru.start()
network = theanets.Experiment(
        theanets.feedforward.Regressor,
        layers=(app.config['IMG_W'] * app.config['IMG_H'], 500, 1)
        )
network = network.load(path="net.data")


from web import views, models