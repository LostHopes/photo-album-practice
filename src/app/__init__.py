from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()



def create_app(config_obj=None):

    app.config.from_object(config_obj)

    with app.app_context():
        from app import views, models

    return app