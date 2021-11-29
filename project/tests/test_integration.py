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
    
    def test_save_data(self):
        response = self.client.get("/")

        self.assert_template_used("index.html")

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
