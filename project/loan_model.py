from . import db
from user_model import User

class Loan(db.Model):

    id              = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id         = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    amount          = db.Column(db.Integer)
    amountt          = db.Column(db.Integer)
    rate            = db.Column(db.Float)
    intent          = db.Column(db.String(100))
    grade           = db.Column(db.String(1))
    start_date      = db.Column(db.Date)