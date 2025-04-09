from flask import Blueprint


album_bp = Blueprint(
    "album_bp",
    __name__,
    template_folder="templates/album",
    static_folder="static/album",
)

from app.album import models, views
