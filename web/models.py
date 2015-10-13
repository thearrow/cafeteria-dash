from web import db
from datetime import datetime, time


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time, index=True)
    data = db.Column(db.Numeric)

    def __init__(self, data):
        self.date = datetime.now().date()
        now = datetime.now().time()
        self.time = time(now.hour, now.minute, 0, 0) # round down to nearest minute
        self.data = data

    def __repr__(self):
        return "Data: {} - {} = {}".format(self.date, self.time, self.data)