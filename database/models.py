from app import db


class testcollection(db.Document):
    test = db.IntField()
