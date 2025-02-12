from app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    registered_date = db.Column(db.DateTime)
    photos = db.relationship("Photos", back_populates="users")

    @login_manager.user_loader
    def load_user():
        return Users.get_id()


class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String)
    user_id = db.Column(db.ForeignKey("user.id"))
    users = db.relationship("User", back_populates="photos")
    category = db.relationship("PhotoCategory", back_populates="photo")

class PhotoCategory(db.Model):
    __tablename__ = "photo_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    photo = db.relationship("Photos", back_populates="category")
