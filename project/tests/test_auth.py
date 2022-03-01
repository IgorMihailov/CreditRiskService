# pytest --cov=project --cov-report=html project/tests/
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from ..user_model import User
from .. import db
from .. import auth

class TestAuth(TestCase):

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

    # Pages GET tests
    def test_get_home(self):
        response = self.client.get("/")

        self.assert_template_used("index.html")

    def test_get_login_page(self):
        response = self.client.get("/login")

        self.assert_template_used("login.html")

    def test_get_signup_page(self):
        response = self.client.get("/signup")

        self.assert_template_used("signup.html")

    def test_logout_without_login(self):
        response = self.client.get("/logout")

        self.assert_redirects(response, "/login?next=%2Flogout")

    def test_get_loans_page(self):
        response = self.client.get("/loans")

        self.assert_template_used("loans.html")

    # Sign up tests
    def test_sign_up_user(self):

        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        response = self.signup_request(email, name, password)
        new_user = db.session.query(User).filter(User.email == email).first()


        self.assertIsNotNone(new_user, 'DB doesn\'t contain new user!')

    def test_sign_up_already_existing_user(self):

        expected_flash_message = 'Email address already exists'

        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        # first user
        response = self.signup_request(email, name, password)

        # second user
        response = self.signup_request(email, name, password)

        users_count = db.session.query(User).count()

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes']).get('error')


        self.assertEqual(users_count, 1)
        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertEqual(flash_message, expected_flash_message)

    # Login tests
    def test_login_user(self):

        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # login
        response = self.login_request(email, password)

        self.assertIsNotNone(current_user, "User didn't login!")
        self.assert_redirects(response, "/profile")

    def test_login_not_existing_user(self):
        expected_flash_message = 'Please check your login details and try again.'

        email = 'new_user@gmail.com'
        password = '123456'

        # login
        response = self.login_request(email, password)

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes']).get('error')

        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertEqual(flash_message, expected_flash_message)

    def test_login_wrong_password(self):
        expected_flash_message = 'Please check your login details and try again.'

        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'
        wrong_password = 'qwerty123'

        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # login
        response = self.login_request(email, wrong_password)

        with self.client.session_transaction() as session:
            flash_message = dict(session['_flashes']).get('error')

        self.assertIsNotNone(flash_message, session['_flashes'])
        self.assertEqual(flash_message, expected_flash_message)

    # Logout tests
    def test_login_then_logout(self):
        email = 'new_user@gmail.com'
        name = 'admin'
        password = '123456'

        new_user = User(email=email,
                        name=name,
                        password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # login
        response = self.login_request(email, password)

        # Logout
        response = self.logout()

        with self.client.session_transaction() as session:
            assert "user_id" not in session
        self.assert_redirects(response, "/")

    def signup_request(self, email, name, password):
        return self.client.post('/signup', data=dict(
            email=email,
            name=name,
            password=password
        ), follow_redirects=False)

    def login_request(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=False)

    def logout(self):
        return self.client.get('/logout', follow_redirects=False)

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
