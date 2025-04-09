from app import db


class PhotoAlbum(db.Model):
    __tablename__ = "photo_album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.Relationship("User", back_populates="albums")
    category = db.Relationship(
        "AlbumCategory", back_populates="album", cascade="all,delete"
    )
    photos = db.Relationship("Photo", back_populates="album", cascade="all,delete")


class AlbumCategory(db.Model):
    __tablename__ = "album_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey("photo_album.id"))
    album = db.Relationship("PhotoAlbum", back_populates="category")


class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    album_id = db.Column(db.Integer, db.ForeignKey("photo_album.id"))
    album = db.Relationship("PhotoAlbum", back_populates="photos")
