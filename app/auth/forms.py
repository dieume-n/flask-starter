from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo

from app.users.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        "Email address",
        validators=[
            DataRequired(message="Email address cannot be empty"),
            Email(message="Please enter a valid email address"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Password cannot be empty")]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Signin")


class RegisterForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired("Name cannot be empty"),
            Length(min=3, message="Name must be atleast 3 characters long"),
        ],
    )
    email = EmailField(
        "Email address",
        validators=[
            DataRequired(message="Email address cannot be empty"),
            Email(message="Please enter a valid email address"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Password cannot be empty")]
    )
    submit = SubmitField("Sign up")

    def validate_email(self, email):
        user = User.find_by_email(email.data)
        if user:
            raise ValidationError("Sorry! this email is already taken.")
        return True


class RequestResetForm(FlaskForm):
    email = EmailField(
        "Email address",
        validators=[
            DataRequired(message="Email address cannot be empty"),
            Email(message="Please enter a valid email address"),
        ],
    )

    submit = SubmitField("Request password reset")

    def validate_email(self, email):
        user = User.find_by_email(email.data)
        if not user:
            raise ValidationError(
                "Sorry! there is no account with that email, you must register first"
            )
        return True


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(message="Password cannot be empty")]
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(message="Password cannot be empty"),
            EqualTo("password"),
        ],
    )
    submit = SubmitField("Reset password")
