import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from ..models import User
from .. import db
from .. import auth

class TestProfile(TestCase):

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

    def test_get_profile_unauth(self):
        response = self.client.get("/profile")
        self.assertMessageFlashed("Please check your login details and try again.", category='error')

    def test_get_profile_unauth(self):
        expected_flash_message = 'Please log in to access this page.'
        response = self.client.get("/profile")

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes']).get('message')

        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertEqual(flash_message, expected_flash_message)

    def test_get_profile_auth(self):
        #self.auth()
        response = self.client.get("/profile")
        self.assert_redirects(response, "/login?next=%2Fprofile")

    def test_get_profile_auth(self):
        self.auth()
        response = self.client.get("/profile")
        self.assert_redirects(response, "/login?next=%2Fprofile")

    def test_save_profile_data(self):
            
        passport = "8614152327"
        phone = "777-888"
        age = "20"
        income = "30000"
        emp_length = "1"
        defaults_in_past = "N"
        hist_length = "0"
          
        self.auth()
        user = User.query.filter_by(email=current_user.email).first()
        response = self.client.post("/profile", data=dict(
                username=user.email,
                password=user.password,
                passport=passport,
                phone=phone,
                age=age,
                income=income,
                emp_length=emp_length,
                defaults_in_past=defaults_in_past,
                hist_length=hist_length
            ), follow_redirects=False)

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes']).get('error')

        self.assertIsNotNone(flash_message, session['_flashes'])
        #self.assertEqual(flash_message, expected_flash_message)
        

    def auth(self):
        email = 'email'
        password = 'password'
        name = 'user'

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        #login_user(new_user)

# # Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
