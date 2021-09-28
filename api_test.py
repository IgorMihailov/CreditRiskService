import requests

json_str = {"person_age":66,"person_income":42000,"person_emp_length":2.0,"loan_amnt":6475,"loan_int_rate":9.99,"loan_percent_income":0.15,"cb_person_cred_hist_length":30,"person_home_ownership_MORTGAGE":0,"person_home_ownership_OTHER":0,"person_home_ownership_OWN":0,"person_home_ownership_RENT":1,"loan_intent_DEBTCONSOLIDATION":0,"loan_intent_EDUCATION":0,"loan_intent_HOMEIMPROVEMENT":0,"loan_intent_MEDICAL":1,"loan_intent_PERSONAL":0,"loan_intent_VENTURE":0,"loan_grade_A":0,"loan_grade_B":1,"loan_grade_C":0,"loan_grade_D":0,"loan_grade_E":0,"loan_grade_F":0,"loan_grade_G":0,"cb_person_default_on_file_N":1,"cb_person_default_on_file_Y":0}

res = requests.post('http://localhost:5000/api/prediction', json=json_str)
if res.ok:
    print(res.json())
