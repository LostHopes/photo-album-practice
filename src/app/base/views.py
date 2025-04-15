from flask import render_template
from app.base import base_bp


@base_bp.get("/")
def home():
    title: str = "Home"
    return render_template("home.html", title=title)
