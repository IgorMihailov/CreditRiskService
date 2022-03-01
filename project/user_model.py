# user_model.py

from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from . import db

class User(UserMixin, db.Model):

    # common data
    id                  = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email               = db.Column(db.String(100), unique=True)
    password            = db.Column(db.String(100))
    name                = db.Column(db.String(1000))
    passport            = db.Column(db.String(11))
    phone               = db.Column(db.String(15))

    # data for prediction
    age                 = db.Column(db.Integer)
    income              = db.Column(db.Integer)
    emp_length          = db.Column(db.Integer)
    defaults_in_past    = db.Column(db.String(1))
    hist_length         = db.Column(db.Integer)

class ProfileForm(FlaskForm):

    """Profile form."""

    passport = StringField(
        'Passport',
        [DataRequired()]
    )

    phone = StringField(
        'Phone',
        [DataRequired()]
    )

    age = StringField(
        'Age',
        [DataRequired()]
    )

    income = StringField(
        'Income',
        [DataRequired()]
    )

    emp_length = StringField(
        'Employee Length',
        [DataRequired()]
    )

    defaults_in_past = SelectField('Defaults in past', choices=[
        ('N', 'No'),
        ('Y', 'Yes'),
    ])

    hist_length = StringField(
        'Credit history length',
        [DataRequired()]
    )

    submit = SubmitField('Submit')
