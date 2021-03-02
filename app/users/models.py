from sqlalchemy import Column, String, Integer, DateTime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.core.model import BaseModel
from app.extensions import login_manager, bcrypt
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(int(user_id))


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    email = Column(String(250), unique=True, index=True)
    confirmed_at = Column(DateTime(), nullable=True)
    password = Column(String(60))

    def __init__(self, name, email, password: str):
        self.name = name.strip().title()
        self.email = email.lower()
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str):
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    @classmethod
    def find_by_email(cls, email: str):
        user = cls.query.filter_by(email=email).first()
        if not user:
            return False
        return user

    def get_reset_token(self):
        serializer = Serializer(
            current_app.config["SECRET_KEY"],
            expires_in=int(current_app.config["RESET_PASSWORD_TOKEN_EXPIRY"]),
        )
        return serializer.dump({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(reset_token):
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(reset_token)["user_id"]
        except IndexError:
            return None

        return User.find_by_id(user_id)

    def __repr__(self):
        return f"<User: {self.name} {self.email}"  # pragma: no cover
