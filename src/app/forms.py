from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField,
    StringField,
    EmailField,
    PasswordField,
    SubmitField,
    FileField,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    StopValidation,
    Regexp,
    Length,
    EqualTo,
    Optional,
)


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=25,
                message="Enter username from %(min)d to %(max)d characters",
            ),
        ],
        render_kw={"placeholder": "Enter username here"},
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(
                min=4, max=254, message="Enter email from %(min)d to %(max)d characters"
            ),
        ],
        render_kw={"placeholder": "Enter email here"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=255,
                message="Password contains not enough or too many characters",
            ),
            EqualTo("confirm_password", message="Passwords aren't the same"),
        ],
        render_kw={"placeholder": "Enter password here"},
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=255,
                message="Password contains not enough or too many characters",
            ),
        ],
        render_kw={"placeholder": "Confirm the password"},
    )
    accept_rules = BooleanField("Accept rules", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter email here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password here"},
    )
    stay_logged_in = BooleanField("Stay logged in", validators=[Optional()])
    submit = SubmitField("Login")


class UploadForm(FlaskForm):
    file = FileField("Select a photo", validators=[DataRequired()])
    submit = SubmitField("Upload")
