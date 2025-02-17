from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, login_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from b2sdk.v2 import B2Api
from app import app, b2, db
from app.forms import RegisterForm, LoginForm, UploadForm


@app.get("/")
def home():
    title: str = "Home"
    return render_template("home.html", title=title)


@app.route("/photos/")
@login_required
def photos():
    title: str = "Photos"
    form = UploadForm()

    bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])

    return render_template("photos.html", title=title, form=form)


@app.post("/photos/")
def upload_photo():
    return redirect(url_for("photos"))


@app.get("/register/")
def register_page():
    title: str = "Register"
    form = RegisterForm()

    if form.validate_on_submit():
        return redirect(url_for("register_page"))

    return render_template("register.html", title=title, form=form)


@app.post("/register/")
def process_register():
    flash("User successfully registered", "success")
    return redirect(url_for("login_page"))


@app.get("/login/")
def login_page():
    title: str = "Login"
    form = LoginForm()

    return render_template("login.html", title=title, form=form)


@app.post("/login/")
def process_login():

    logout_user()

    flash("User successfully logged in")
    return redirect(url_for("photos"))


@app.post("/logout/")
@login_required
def logout():
    logout_user()
    flash("You succesfully logged out", "success")
    return redirect(url_for("login_page"))
