from . import db

class Loan(db.Model):

    __tablename__ = 'loans'
    id              = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_id         = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user            = db.relationship("User", back_populates="loans")

    amount          = db.Column(db.Integer)
    rate            = db.Column(db.Float)
    intent          = db.Column(db.String(100))
    grade           = db.Column(db.String(1))
    start_date      = db.Column(db.Date)