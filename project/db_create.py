from . import create_app, db, loan_model, user_model
app = create_app()
db.drop_all(app=app)
db.create_all(app=app)