from flask import flash, request, render_template, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.user import user_bp
from app.user.models import User
from app.user.forms import RegisterForm, LoginForm
from app import app, db


@user_bp.route("/register/", methods=["GET", "POST"])
def register_page():
    title: str = "Register"
    form = RegisterForm()

    try:
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password_hash = generate_password_hash(form.password.data)

            user = User(username=username, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()

            app.logger.info(f"The user {username} has been registered")
            flash("User successfully registered", "success")
            return redirect(url_for("user_bp.login_page"))

    except IntegrityError:
        db.session.rollback()
        flash("User with this username or email already exists", "error")

    return render_template("register.html", title=title, form=form)


@user_bp.get("/login/")
def login_page():
    title: str = "Login"
    form = LoginForm()

    return render_template("login.html", title=title, form=form)


@user_bp.post("/login/")
def process_login():
    form = LoginForm(request.form)

    user = (
        db.session.query(User)
        .filter_by(email=form.email.data)
        .first_or_404(description="User not found")
    )

    if not check_password_hash(user.password, form.password.data):
        flash("The password is wrong or user doesn't exist", "error")
        return redirect(url_for("user_bp.login_page"))

    login_user(user, remember=form.stay_logged_in.data)

    app.logger.info(f"User {user.username} has logged in")
    flash("User successfully logged in", "success")
    return redirect(url_for("album_bp.photos"))


@user_bp.post("/logout/")
@login_required
def logout():
    logout_user()
    flash("You succesfully logged out", "success")
    return redirect(url_for("user_bp.login_page"))


@user_bp.get("/account/")
@login_required
def account():
    title: str = "Account"
    return render_template("account.html", title=title, username=current_user.username)
