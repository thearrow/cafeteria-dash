from web import app, db, session, network
from web.models import Data
from flask import render_template, send_from_directory, jsonify
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
from sqlalchemy.sql import func
from datetime import datetime
import util_guru
import util_image
import time
import glob
import os
import json
import theanets
import requests
from bs4 import BeautifulSoup


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/current")
def current():
    for file in glob.glob("web/static/img/*.jpg"):
        os.remove(file)
    image = util_guru.download(session)
    timestamp = time.time()
    file = "web/static/img/img-{}.jpg".format(timestamp)
    util_image.save(image, file)
    imageFile = "static/img/img-{}.jpg".format(timestamp)
    input = util_image.get_single_input_data(image)
    output = network.predict(input)[0][0]
    return jsonify(currentImg=imageFile, currentNum=output)


@app.route("/weather")
def weather():
    weatherData = cache.get('weather')
    if weatherData is None:
        api_key = app.config['WEATHER_API_KEY']
        api_url = "http://api.wunderground.com/api/{}/conditions/q/pws:KWIVERON5.json".format(api_key)
        app.logger.info(api_url)
        response = requests.get(api_url)
        weatherData = response.json()
        cache.set('weather', weatherData, timeout=300) # cache will last 5 minutes
    return jsonify(weatherData)


@app.route("/menu")
def menu():
    menuData = cache.get('menu')
    if menuData is None:
        html = session.get("http://teamportal/sites/admin/Culinary/Lists/Menu Items/Simplified.aspx").text
        soup = BeautifulSoup(html)
        today = datetime.today()
        today_str = " : {}/{}/{}".format(today.month, today.day, today.year)
        today_element = soup.find_all(text=today_str, limit=1)
        menu_tbody = today_element[0].parent.parent.parent.next_sibling
        menuData = {}
        for tr in menu_tbody.next_siblings:
            if not tr.contents:
                break
            if not tr.contents[0].string:
                continue
            category = tr.contents[0].string
            name = tr.contents[1].string
            price = tr.contents[2].string
            if category in menuData:
                menuData[category].append((name, price))
            else:
                menuData[category] = [(name, price)]
        menuData = json.dumps(menuData)
        cache.set('menu', menuData , timeout=14400) # cache will last 4 hours
    return menuData


@app.route("/date/<date>")
def date(date):
    try:
        dt = datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        abort(500)

    data = []
    dataList = Data.query.filter_by(date=dt.date())
    for d in dataList:
        dt = datetime.combine(d.date, d.time)
        data.append({ 'time':dt.isoformat(), 'data':d.data }) #.strftime("%Y-%m-%d %H:%M:%S")

    days = get_days()
    averageData = get_averages(dt.date())
    return jsonify(data=[data, averageData], days=days)


@app.route("/stats")
def stats():
    days = get_days()
    averageData = get_averages(datetime.now().date())
    return jsonify(days=days, averages=averageData)


def get_days():
    days = cache.get('days')
    if days is None:
        days = Data.query.group_by(Data.date).count()
        cache.set('days', days, timeout=28800) # cache will last 8 hours
    return days


def get_averages(date):
    averagesKey = "averages-{}".format(date.day)
    averageData = cache.get(averagesKey)
    if averageData is None:
        averageData = []
        averages = db.session.query(Data.time, func.avg(Data.data)).group_by(Data.time).all()
        for avg in averages:
            dt = datetime.combine(date, avg[0])
            averageData.append({ 'time':dt.isoformat(), 'data':avg[1] })
        cache.set(averagesKey, averageData, timeout=28800) # cache will last 8 hours
    return averageData