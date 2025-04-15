from flask import Blueprint


base_bp = Blueprint(
    "base_bp",
    __name__,
    template_folder="templates/base",
    static_folder="static/base"
)

from app.base import views, errors