# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
   
    # common data
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    passport = db.Column(db.String(11))
    phone = db.column(db.String(15))

    # data for prediction
    age                 = db.column(db.Integer)
    income              = db.column(db.Integer)
    emp_length          = db.column(db.Integer)	
    loan_grade          = db.column(db.String(1))
    defaults_in_past    = db.column(db.String(1))
    hist_length         = db.column(db.Integer)