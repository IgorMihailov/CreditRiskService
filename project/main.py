# main.py

import copy
from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import ProfileForm
from .models import User
from . import db
from .validation_service import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = ProfileForm(request.form)

    # when get
    if request.method == "GET":
        if current_user.passport != None:
            form.passport.data=current_user.passport.replace("_", "")

        form.phone.data=current_user.phone
        form.age.data=current_user.age
        form.income.data=current_user.income
        form.emp_length.data=current_user.emp_length
        form.defaults_in_past.data=current_user.defaults_in_past
        form.hist_length.data=current_user.hist_length

        return render_template('profile.html', form=form, name=current_user.name)

    # when post
    if request.method == "POST": #form.validate_on_submit():

        if not check_length(form.passport.data):
            flash ("Passport must bе 10 numbers!")
            return redirect(url_for('main.profile'))

        if not is_passport_valid(form.passport.data):
            flash ("Passport in expired list!")
            return redirect(url_for('main.profile'))

        user = User.query.filter_by(email=current_user.email).first()
        user.passport = form.passport.data
        user.phone = form.phone.data
        user.age = form.age.data
        user.income = form.income.data
        user.emp_length = form.emp_length.data
        user.defaults_in_past = form.defaults_in_past.data
        user.hist_length = form.hist_length.data

        db.session.commit()
        flash("Saved successfully!")
        return redirect(url_for('main.profile'))

    return render_template('index.html')
