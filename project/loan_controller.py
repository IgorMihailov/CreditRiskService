import sys
from flask import Blueprint, render_template, request, make_response
from flask_login import login_required, current_user

from .loan_model import Loan
from .user_model import User
from . import db
from . import loan_service

loan = Blueprint('loan', __name__)

@loan.route('/loans_list')
@login_required
def loans():
    return render_template('new-loans.html')

@loan.route('/user_loans_list')
@login_required
def user_loans():
    loans = loan_service.get_curr_user_loans()
    return render_template('user-loans.html', loans=loans)

@loan.route('/add_loan', methods=['POST'])
@login_required
def add_loan():
    loan_data = request.get_json()
    result = loan_service.create_loan(loan_data)

    response = make_response(result, 200)
    response.mimetype = "text/plain"
    return response
