from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_message = "You can't view the photo album page as guest"
login_manager.login_message_category = "error"


def create_app(config_obj=None):
    app.config.from_object(config_obj)

    with app.app_context():
        from app import views, models

        db.init_app(app)
        login_manager.init_app(app)
        bcrypt.init_app(app)

        db.create_all()

    return app
