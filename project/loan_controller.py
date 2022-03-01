from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .user_model import User
from . import db

loan = Blueprint('loan', __name__)

@loan.route('/add_loan')
def login():
    return render_template('index.html')
