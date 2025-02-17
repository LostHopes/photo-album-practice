from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, login_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from b2sdk.v2 import B2Api, B2Folder
from app import app, b2, db
from app.forms import RegisterForm, LoginForm, UploadForm
from app.models import User, Photo


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
    try:
        form = RegisterForm(request.form)

        if form.validate():
            username = form.username.data
            email = form.email.data
            password_hash = generate_password_hash(form.password.data)
            confirm_password = form.confirm_password.data

            user = User(username=username, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()

            flash("User successfully registered", "success")
            return redirect(url_for("login_page"))

    except IntegrityError:
        db.session.rollback()
        flash("User already exist", "error")
    return redirect(url_for("register_page"))


@app.get("/login/")
def login_page():
    title: str = "Login"
    form = LoginForm()

    return render_template("login.html", title=title, form=form)


@app.post("/login/")
def process_login():
    form = LoginForm(request.form)

    user = (
        db.session.query(User)
        .filter_by(email=form.email.data)
        .first_or_404(description="User not found")
    )

    if not check_password_hash(user.password, form.password.data):
        flash("Password is wrong or user doesn't exist", "error")
        return redirect(url_for("login_page"))

    login_user(user, remember=form.stay_logged_in.data)

    flash("User successfully logged in", "success")
    return redirect(url_for("photos"))


@app.post("/logout/")
@login_required
def logout():
    logout_user()
    flash("You succesfully logged out", "success")
    return redirect(url_for("login_page"))
