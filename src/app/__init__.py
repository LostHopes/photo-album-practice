from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from b2sdk.v2 import B2Api
import sys


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
b2 = B2Api()

login_manager.login_view = "user_bp.login_page"
login_manager.login_message = "You can't view the photo album page as guest"
login_manager.login_message_category = "info"


def create_app(config_obj=None):
    app.config.from_object(config_obj)

    with app.app_context():
        from app.user import user_bp
        from app.album import album_bp
        from app.base import base_bp

        app.register_blueprint(base_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(album_bp)

        db.init_app(app)
        login_manager.init_app(app)
        bcrypt.init_app(app)
        migrate.init_app(app, db)

        if "pytest" not in sys.modules:
            b2.authorize_account(
                "production", app.config["B2_KEY_ID"], app.config["B2_KEY"]
            )

        db.create_all()

    return app
