from flask import render_template
from app import app


@app.errorhandler(404)
def page_not_found(msg):
    return render_template("error.html", msg=msg)


@app.errorhandler(401)
def user_unauthorized(msg):
    return render_template("error.html", msg=msg)
