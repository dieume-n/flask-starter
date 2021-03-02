from flask import Blueprint, render_template
from flask_login import login_required

from app.users.models import User

users_bp = Blueprint("users", __name__)


@users_bp.route("/account")
@login_required
def home():
    return render_template("users/home.html")
