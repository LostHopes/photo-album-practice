from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, login_remembered, login_user
from flask_bcrypt import generate_password_hash, check_password_hash
from app import app
from app.forms import RegisterForm, LoginForm, UploadForm


@app.get("/")
def home():
    title: str = "Home"
    return render_template("home.html", title=title)


@app.get("/photos/")
def photos():
    title: str = "Photos"
    form = UploadForm()

    return render_template("photos.html", title=title, form=form)


@app.post("/photos/")
def process_upload():
    return redirect(url_for("photos"))


@app.get("/register/")
def register_page():
    title: str = "Register"
    form = RegisterForm()

    return render_template("register.html", title=title, form=form)


@app.post("/register/")
def process_register():
    return redirect(url_for("register_page"))


@app.get("/login/")
def login_page():
    title: str = "Login"
    form = LoginForm()

    return render_template("login.html", title=title, form=form)


@app.post("/login/")
def process_login():
    return redirect(url_for("photos"))
