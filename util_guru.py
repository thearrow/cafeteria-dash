import config
import requests
from requests_ntlm import HttpNtlmAuth
import time
import getpass
from StringIO import StringIO
from PIL import Image


def start():
    session = requests.Session()
    print "The Cassiopeia webcam requires authentication..."
    username = raw_input("Your windows username: ")
    password = getpass.getpass("Your windows password: ")
    session.auth = HttpNtlmAuth("epic\\{}".format(username), password, session)
    return session


def download(session):
    data = session.get(config.IMG_URL)
    image = Image.open(StringIO(data.content))
    return image