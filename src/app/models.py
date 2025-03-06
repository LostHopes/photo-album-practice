from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    registered_date = db.Column(
        db.DateTime, default=datetime.now().replace(microsecond=0)
    )
    albums = db.relationship("PhotoAlbum", back_populates="user", cascade="all,delete")

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).filter_by(id=user_id).first()


class PhotoAlbum(db.Model):
    __tablename__ = "photo_album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.Relationship("User", back_populates="albums")
    category = db.Relationship("AlbumCategory", back_populates="album", cascade="all,delete")
    photos = db.Relationship("Photo", back_populates="album", cascade="all,delete")


class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey("photo_album.id"))
    album = db.Relationship("PhotoAlbum", back_populates="photos")


class AlbumCategory(db.Model):
    __tablename__ = "album_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey("photo_album.id"))
    album = db.Relationship("PhotoAlbum", back_populates="category")
