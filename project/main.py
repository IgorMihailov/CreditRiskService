# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import ProfileForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():

    form = ProfileForm()

    # when post
    if form.validate_on_submit():
        flash("Success", "Error")
        return render_template('profile.html', form=form, name=current_user.name)

    # when get
    form.passport.data=current_user.passport.replace("_", "")
    form.phone.data=current_user.phone
    form.age.data=current_user.age
    form.income.data=current_user.income
    form.emp_length.data=current_user.emp_length
    form.defaults_in_past.data=current_user.defaults_in_past
    form.hist_length.data=current_user.hist_length

    return render_template('profile.html', form=form, name=current_user.name)
