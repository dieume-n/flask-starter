from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from app.auth.forms import LoginForm, RegisterForm, RequestResetForm, PasswordResetForm
from app.users.models import User
from app.core.helpers import send_welcome_email


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)

        if user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("users.home"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = {
            "name": form.name.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        registered_user = User(**user)
        registered_user.save()
        send_welcome_email(user["name"], user["email"])

        flash("Registration successful, please login", category="success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():

    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/password-reset", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        pass
    return render_template("auth/reset-request.html", form=form)


@auth_bp.route("/password-reset/<string:token>", methods=["GET", "POST"])
def password_reset(token: str):
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))

    # user = User.verify_reset_token(token)
    # if not user:
    #     flash("invalid or expired token", "warning")
    #     return redirect(url_for("auth.reset_request"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        pass
    return render_template("auth/password-reset.html", form=form)