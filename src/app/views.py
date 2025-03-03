from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from b2sdk.v2 import B2Api, B2Folder
from app import app, b2, db
from app.forms import RegisterForm, LoginForm, UploadForm, AlbumForm
from app.models import User, Photo, PhotoAlbum


@app.get("/")
def home():
    title: str = "Home"
    return render_template("home.html", title=title)


@app.get("/account/")
@login_required
def account():
    title: str = "Account"
    return render_template("account.html", title=title)


@app.get("/albums/")
@login_required
def photos():
    title: str = "Albums"

    form = AlbumForm()

    albums = db.session.query(PhotoAlbum).filter_by(user_id=current_user.get_id()).all()

    return render_template("photos.html", title=title, form=form, albums=albums)


@app.get("/albums/<int:album_id>/")
@login_required
def album_page(album_id: int):
    title: str = "Album"
    form = UploadForm()
    bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])
    names = db.session.query(Photo).filter_by(album_id=album_id).all()

    urls: list[str] = []
    token = b2.account_info.get_account_auth_token()
    for image in names:
        urls.append(f"{bucket.get_download_url(image.name)}?Authorization={token}")

    if form.validate_on_submit():
        return redirect("process_upload", album_id=album_id)

    return render_template("album.html", title=title, form=form, urls=urls)


@app.post("/albums/<int:album_id>/")
@login_required
def process_upload(album_id: int):
    files = request.files.getlist("file")

    bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])

    for f in files:
        photo = Photo(name=f.filename, album_id=album_id)
        db.session.add(photo)
        db.session.commit()
        bucket.upload_bytes(data_bytes=f.read(), file_name=f.filename)

    return redirect(url_for("photos"))


@app.get("/albums/create")
@login_required
def create_album():
    title: str = "Create album"
    form = AlbumForm()

    if form.validate_on_submit():
        return redirect(url_for("process_album"))

    return render_template("create.html", title=title, form=form)


@app.post("/albums/create")
@login_required
def process_album():
    try:
        form = AlbumForm(request.form)
        name = form.name.data
        category = form.category.data

        album = PhotoAlbum(name=name, user_id=current_user.get_id())
        db.session.add(album)
        db.session.commit()

    except IntegrityError:
        flash("Album with a given name already exist", "error")
        return redirect(url_for("photos"))

    flash("Album was created successfully", "success")
    return redirect(url_for("photos"))


@app.post("/albums/remove/<int:album_id>/")
@login_required
def remove_album(album_id: int):
    try:
        album = db.session.query(PhotoAlbum).filter_by(id=album_id).first()
        db.session.delete(album)
        db.session.commit()
        flash("The album was successfully deleted", "success")

    except Exception as e:
        flash("Failed to remove the album", "error")
    return redirect(url_for("photos"))



@app.post("/albums/<int:album_id>/remove")
def remove_photo(album_id: int):

    bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])
    photo = db.session.query(Photo).filter_by(album_id=album_id).first()
    filename = bucket.get_file_info_by_name(photo.name)

    return redirect(url_for("album_page"))


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
        flash("User with this username or email already exist", "error")
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
        flash("The password is wrong or user doesn't exist", "error")
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
