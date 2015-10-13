# About
A fun little project to create a one-stop dashboard for a cafeteria, including crowd levels (current and historical averages), current weather, and today's menu.


# How Does This Work?
Every minute from 10:30am to 2:00pm (when the cafeteria is open), a python script connects to the cafeteria webcam and downloads an image. The image is preprocessed (resized and converted to grayscale) and fed to an artificial neural network that was trained on some manually-labeled data. The neural network returns its best guess at how crowded the image looks (on a scale of 1-10), and this result is saved to a database. The dashboard queries the database and generates some lovely graphs.

Current weather conditions for the cafeteria location (to help the viewer to decide whether or not to sit outside) are pulled from the Weather Underground API.

Today's menu for the cafeteria is screen-scraped from the intranet site.


# Screenshot
![Example Screenshot](http://i.imgur.com/epOgRn4.png "Example Screenshot")


# Setup

Install Anaconda:
https://store.continuum.io/cshop/anaconda/

Install Theano:
http://deeplearning.net/software/theano/install.html#bleeding-edge-installation

Install Curses:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses

pip install:
requests
requests_ntlm
pillow
theanets
flask
flask-sqlalchemy
sqlalchemy-migrate
simplejson
beautifulsoup4