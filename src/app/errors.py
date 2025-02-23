from flask import render_template
from app import app


@app.errorhandler(404)
def page_not_found(msg):
    title: str = "Error 404"
    return render_template("error.html", msg=msg, title=title)


@app.errorhandler(401)
def user_unauthorized(msg):
    title: str = "Error 401"
    return render_template("error.html", msg=msg, title=title)
