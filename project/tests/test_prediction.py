import unittest
from flask_testing import TestCase
from flask import Flask
from .. import prediction

class TestPrediction(TestCase):

    render_templates = False

    def create_app(self):
        app = Flask(__name__, template_folder='../templates')

        return app

    # Each test method starts with the keyword test_

    # 0 - accept loan
    # 1 - decline loans

    def test_prediction_positive_data(self):

        data_str = {"person_age":66,
                    "person_income":42000,
                    "person_emp_length":2.0,
                    "loan_amnt":6475,
                    "loan_int_rate":9.99,
                    "loan_percent_income":0.15,
                    "cb_person_cred_hist_length":30,
                    "person_home_ownership": "RENT",
                    "loan_intent": "MEDICAL",
                    "loan_grade": "B",
                    "cb_person_default_on_file": "N"}

        prediction_result = prediction.predict(data_str)

        self.assertEqual(prediction_result, 0)

    def test_prediction_negative_data(self):

        data_str = {"person_age":100,
                    "person_income":0,
                    "person_emp_length":0,
                    "loan_amnt":0,
                    "loan_int_rate":10,
                    "loan_percent_income":0.15,
                    "cb_person_cred_hist_length":0,
                    "person_home_ownership": "RENT",
                    "loan_intent": "MEDICAL",
                    "loan_grade": "B",
                    "cb_person_default_on_file": "Y"}

        prediction_result = prediction.predict(data_str)

        self.assertEqual(prediction_result, 1)

    def test_prediction_bad_input(self):

        data_str = {"person_age":-1}

        prediction_result = prediction.predict(data_str)

        self.assertEqual(prediction_result, -1)

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
