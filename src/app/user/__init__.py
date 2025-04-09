from flask import Blueprint


user_bp = Blueprint(
    "user_bp",
    __name__,
    template_folder="templates/user",
    static_folder="static/user"
)

from app.user import models, views