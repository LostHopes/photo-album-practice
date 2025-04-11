from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from flask_wtf.file import FileAllowed


class UploadForm(FlaskForm):
    file = FileField(
        "Select a photo",
        validators=[
            DataRequired(),
            FileAllowed(
                ["jpg", "png", "jpeg", "webp"],
                message="File extension isn't in the list: jpg, jpeg, png, webp",
            ),
        ],
        render_kw={"multiple": True},
    )
    submit = SubmitField("Upload")


class AlbumForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=6, max=50, message="The name of the album is too long"),
        ],
        render_kw={"placeholder": "Enter the name for an album"},
    )
    category = StringField(
        "Category",
        validators=[
            DataRequired(),
            Length(min=4, max=20, message="The category for the album is too long"),
        ],
        render_kw={"placeholder": "Enter the category for an album"},
    )
    submit = SubmitField("Create album")
