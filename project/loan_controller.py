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
    return render_template('loans.html')

@loan.route('/add_loan', methods=['POST'])
@login_required
def add_loan():
    loan_data = request.get_json()
    print(loan_data, file=sys.stdout)
    result = loan_service.create_loan(loan_data)
    print(result, file=sys.stdout)

    response = make_response(result, 200)
    response.mimetype = "text/plain"
    return response
    #return result, 200
