# pytest --cov=project --cov-report=html project/tests/test_integration.py
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from ..models import User
from .. import db
from .. import auth
from .. import prediction

class TestInt(TestCase):

    render_templates = False

    def create_app(self):
        app = Flask(__name__, template_folder='../templates')

        app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        # blueprint for auth routes in our app
        from ..auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from ..main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Each test method starts with the keyword test_

    def test_save_and_predict_success(self):

        # auth data
        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        # profile data
        phone = '777-333'
        passport = '8614152326'
        age = 10
        income = 150
        emp_length = 0
        defaults_in_past = 'Y'
        hist_length = 0

        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # login
        response = self.login_request(email, password)

        self.assertIsNotNone(current_user, "User didn't login!")
        self.assert_template_used("profile.html")

        # save data
        user_data = dict(
            email = email,
            name = name,
            phone = phone,
            passport = passport,
            age = age,
            income = income,
            emp_length = emp_length,
            defaults_in_past = defaults_in_past,
            hist_length = hist_length)

        response = self.profile_save_request(user_data)

        with self.client.session_transaction() as session:
                flash_message = dict(session['_flashes']).get('message')

        cur_user = db.session.query(User).filter(User.email == email).first()

        # current template
        self.assert_template_used("profile.html")

        # message on page
        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertMessageFlashed("Saved successfully!", 'message')

        # check data in db
        self.assertEqual(cur_user.phone, phone)
        self.assertEqual(cur_user.passport, passport)
        self.assertEqual(cur_user.age, age)
        self.assertEqual(cur_user.income, income)
        self.assertEqual(cur_user.emp_length, emp_length)
        self.assertEqual(cur_user.defaults_in_past, defaults_in_past)
        self.assertEqual(cur_user.hist_length, hist_length)

        # predict for loan
        data_str = {"person_age":cur_user.age,
                    "person_income":cur_user.income,
                    "person_emp_length":cur_user.emp_length,
                    "loan_amnt":6475000,
                    "loan_int_rate":9.999,
                    "loan_percent_income":0.9,
                    "cb_person_cred_hist_length":cur_user.hist_length,
                    "person_home_ownership": "RENT",
                    "loan_intent": "MEDICAL",
                    "loan_grade": "E",
                    "cb_person_default_on_file": cur_user.defaults_in_past}

        prediction_result = prediction.predict(data_str)

        self.assertEqual(prediction_result, 1)

    def test_save_data_passport_expired(self):

        # auth data
        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        # profile data
        passport = '8614152327' # in expired list

        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # login
        response = self.login_request(email, password)

        self.assertIsNotNone(current_user, "User didn't login!")
        self.assert_template_used("profile.html")

        # save data
        user_data = dict(
            email = email,
            name = name,
            passport = passport)

        response = self.profile_save_request(user_data)

        with self.client.session_transaction() as session:
                flash_message = dict(session['_flashes']).get('error')

        cur_user = db.session.query(User).filter(User.email == email).first()

        self.assert_template_used("profile.html")

        # message on page
        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertMessageFlashed("Passport in expired list!", 'error')

        # passport didn't write to db
        self.assertIsNone(cur_user.passport, cur_user)

    def test_save_data_passport_wrong(self):

        # auth data
        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        # profile data
        passport = '12345' # in expired list

        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # login
        response = self.login_request(email, password)

        self.assertIsNotNone(current_user, "User didn't login!")
        self.assert_template_used("profile.html")

        # save data
        user_data = dict(
            email = email,
            name = name,
            passport = passport)

        response = self.profile_save_request(user_data)

        with self.client.session_transaction() as session:
                flash_message = dict(session['_flashes']).get('error')

        cur_user = db.session.query(User).filter(User.email == email).first()

        self.assert_template_used("profile.html")

        # message on page
        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertMessageFlashed("Passport must bе 10 numbers!", 'error')

        # passport didn't write to db
        self.assertIsNone(cur_user.passport, cur_user)

    def login_request(self, email, password):
        return self.client.post('/login', data=dict(
                email=email,
            password=password
        ), follow_redirects=True)

    def profile_save_request(self, user_data):
        return self.client.post('/profile', data = user_data, follow_redirects = True)

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
