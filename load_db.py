from web import db, session, network
from web.models import Data
import theanets
import util_guru
import util_image
import datetime
import time
import threading


def save_to_db():
    threading.Timer(60.0, save_to_db).start() # save one data point per minute
    if time_to_save_data():
        image = util_guru.download(session)
        input = util_image.get_single_input_data(image)
        output = network.predict(input)[0][0]
        d = Data(output)
        print "Adding ", time.strftime("%m/%d %H:%M:%S", time.localtime()), " => ", output, "..."
        db.session.add(d)
        db.session.commit()


def time_to_save_data():
    now = datetime.datetime.now()
    if is_between_1030_and_1400(now) and is_weekday(now):
        return True 
    return False


def is_between_1030_and_1400(dt):
    hour = dt.time().hour
    min = dt.time().minute
    if hour == 10 and min >= 30:    # 10:30 - 10:59
        return True
    if 11 <= hour and hour < 14 :   # 11:00 - 14:00
        return True
    return False


def is_weekday(dt):
    weekday = dt.isoweekday()
    if 1 <= weekday and weekday <= 5:  # Mon - Fri
        return True
    return False
    

save_to_db()