from . import db

class Loan(db.Model):

    id              = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    amount          = db.Column(db.Integer)
    rate            = db.Column(db.Float)
    intent          = db.Column(db.String(100))
    grade           = db.Column(db.String(1))