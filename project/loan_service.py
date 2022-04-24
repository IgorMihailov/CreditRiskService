from numpy import true_divide
from . import prediction
from . import db
import sys
from flask_login import current_user
from .loan_model import Loan
from datetime import date

def get_curr_user_loans():
  user = current_user
  print (user.id, file=sys.stdout)
  loans = Loan.query.filter_by(user_id=user.id).all()
  return loans

def create_loan(loan_data):
    
    if (not approve_loan(loan_data)):
      return "Not approved"

    user = current_user
    amount = loan_data['amount']
    rate = loan_data['rate']
    intent = loan_data['intent']
    grade = loan_data['grade']

    new_loan = Loan(user=user, user_id=user.id, amount=amount, rate=rate, intent=intent, grade=grade, start_date=date.today())
    db.session.add(new_loan)
    db.session.commit()
    
    print(new_loan, file=sys.stdout)
    return "Approved"

def delete_loan(loan_id):
    return None

def update_loan(loan_data, loan_id):
    return None

def approve_loan(loan_data):
  user = current_user
  data_str = {"person_age":user.age,
              "person_income":user.income,
              "person_emp_length":user.emp_length,
              "loan_amnt":loan_data['amount'],
              "loan_int_rate":loan_data['rate'],
              "loan_percent_income":0.1,
              "cb_person_cred_hist_length":user.hist_length,
              "person_home_ownership": "RENT",
              "loan_intent": loan_data['intent'],
              "loan_grade": loan_data['grade'],
              "cb_person_default_on_file": user.defaults_in_past}

  prediction_result = prediction.predict(data_str)  

  if prediction_result == 0:
    return True
  else: 
    return False