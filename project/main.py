# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
    name=current_user.name,
    passport=current_user.passport.replace("_", ""),
    phone=current_user.phone,
    age=current_user.age,
    income=current_user.income,
    emp_length=current_user.emp_length,
    defaults_in_past=current_user.defaults_in_past,
    hist_length=current_user.hist_length)
