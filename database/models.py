# Python 3.7.4
from app import db


class testcollection(db.Document):
    test = db.IntField()
    title = db.StringField()

class Auction(db.Document):
    status = db.StringField()
    link = db.URLField()
    source = db.StringField()
    title = db.StringField()
    currentBid = db.IntField()
    startingBid = db.IntField()
    description = db.StringField()
    evaluation = db.IntField()
    auction1Opening = db.DateTimeField()
    auction1Closure = db.DateTimeField()
    auction1Bid = db.IntField()
    auction2Opening = db.DateTimeField()
    auction2Closure = db.DateTimeField()
    auction2Bid = db.IntField()

