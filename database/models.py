# Python 3.7.4
from app import db
from datetime import datetime

class testcollection(db.Document):
    test = db.IntField()
    title = db.StringField()

class Auction(db.Document):
    status = db.StringField()
    url = db.URLField(required=True, unique=True)
    source = db.StringField(required=True)
    title = db.StringField(required=True, unique=True)
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
    createdAt = db.DateTimeField(default=datetime.utcnow)
    disabled = db.BooleanField(default=False)
