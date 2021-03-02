import pytest
from flask import url_for

from app import create_app
from app.extensions import db
from app.users.models import User


@pytest.fixture
def app():
    return create_app("test")


@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture
def user_dict():
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret",
    }


@pytest.fixture
def new_user(user_dict):
    user = User(**user_dict)
    return user


@pytest.fixture
def create_user(user_dict):
    user = User(**user_dict)
    user.save()
    return user


@pytest.fixture
def authenticated_request(client, create_user):
    client.post(
        url_for("auth.login"),
        data=dict(email=create_user.email, password="secret"),
        follow_redirects=True,
    )
    yield client