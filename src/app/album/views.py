from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.album import album_bp
from app.album.models import PhotoAlbum, AlbumCategory, Photo
from app.forms import AlbumForm, UploadForm
from app import app, db, b2


@album_bp.get("/albums/")
@login_required
def photos():
    title: str = "Albums"
    form = AlbumForm()
    per_page = 9
    page = request.args.get("page", 1, int)

    albums = db.paginate(
        db.select(PhotoAlbum)
        .order_by(PhotoAlbum.id)
        .filter_by(user_id=current_user.get_id()),
        per_page=per_page,
        page=page,
    )
    count_photos = lambda id: db.session.query(Photo).filter_by(album_id=id).count()

    return render_template(
        "photos.html",
        title=title,
        form=form,
        albums=albums,
        count_photos=count_photos,
        page=page,
    )


@album_bp.get("/albums/<int:album_id>/")
@login_required
def album_page(album_id: int):
    title: str = "Album"
    form = UploadForm()
    bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])

    # User can't see albums of other users.
    # Rewrite this logic with public and private options (add access field to the album) in the model
    album = (
        db.session.query(PhotoAlbum)
        .filter_by(user_id=current_user.id, id=album_id)
        .first_or_404(description="Album doesn't exist or you don't have access")
    )

    album_data = (
        db.session.query(AlbumCategory, Photo)
        .join(Photo, AlbumCategory.album_id == Photo.album_id)
        .filter(AlbumCategory.album_id == album_id)
        .all()
    )

    urls: list[str] = []
    token = b2.account_info.get_account_auth_token()

    # Here Authorization only for private bucket
    for album, photo in album_data:
        urls.append(
            f"{bucket.get_download_url(f'{album.category}/{photo.name}')}?Authorization={token}"
        )

    return render_template(
        "album.html", title=title, form=form, urls=urls, album_id=album_id
    )


@album_bp.post("/albums/<int:album_id>/")
@login_required
def process_upload(album_id: int):
    try:
        form = UploadForm()

        if form.validate():
            files = request.files.getlist("file")
            bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])
            album = db.session.query(AlbumCategory).filter_by(album_id=album_id).first()

            for f in files:
                photo = Photo(name=f.filename, album_id=album_id)
                db.session.add(photo)
                db.session.commit()
                bucket.upload_bytes(
                    data_bytes=f.read(), file_name=f"{album.category}/{f.filename}"
                )
            flash("The files was successfully uploaded", "success")

    except IntegrityError as e:
        flash("Can't upload a photo to an album", "error")
        app.logger.error(f"Can't upload a photo: {e}")
        db.session.rollback()

    return redirect(url_for("album_bp.photos"))


@album_bp.get("/albums/create/")
@login_required
def create_album():
    title: str = "Create album"
    form = AlbumForm()

    if form.validate_on_submit():
        return redirect(url_for("album_bp.process_album"))

    return render_template("create.html", title=title, form=form)


@album_bp.post("/albums/create/")
@login_required
def process_album():
    try:
        form = AlbumForm(request.form)
        name = form.name.data
        category = form.category.data

        album = PhotoAlbum(name=name, user_id=current_user.get_id())
        db.session.add(album)
        db.session.commit()

        album_category = AlbumCategory(category=category, album_id=album.id)
        db.session.add(album_category)
        db.session.commit()
        flash("Album was created successfully", "success")

    except IntegrityError:
        flash("Album with a given name already exist", "error")
        db.session.rollback()

    return redirect(url_for("album_bp.photos"))


@album_bp.post("/albums/remove/<int:album_id>/")
@login_required
def remove_album(album_id: int):
    try:
        bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])
        album = db.session.query(AlbumCategory).filter_by(album_id=album_id).first()

        for folder, _ in bucket.ls(f"{album.category}/", recursive=True):
            if folder is not None:
                bucket.delete_file_version(folder.id_, folder.file_name)

        album = db.session.query(PhotoAlbum).filter_by(id=album_id).first()
        db.session.delete(album)
        db.session.commit()
        flash("The album was successfully deleted", "success")

    except Exception as e:
        app.logger.error(f"The album can't be deleted: {e}")
        flash("Failed to remove the album", "error")
    return redirect(url_for("album_bp.photos"))


@album_bp.post("/albums/<int:album_id>/remove/")
def remove_photo(album_id: int):
    filename = request.form.get("filename")
    try:
        bucket = b2.get_bucket_by_id(app.config["BUCKET_ID"])

        result = (
            db.session.query(AlbumCategory, Photo)
            .join(AlbumCategory, AlbumCategory.album_id == Photo.album_id)
            .filter(Photo.name == filename, Photo.album_id == album_id)
            .first()
        )

        if result:
            album, photo = result

            db.session.delete(photo)
            db.session.commit()

            file = bucket.get_file_info_by_name(f"{album.category}/{filename}")
            file.delete()

    except IntegrityError as e:
        flash("Can't delete the photo from the album", "error")
        app.logger.error(f"The photo can't be deleted: {e}")
        db.session.rollback()

    return redirect(url_for("album_bp.album_page", album_id=album_id))
