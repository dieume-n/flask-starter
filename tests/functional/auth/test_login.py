import pytest
from flask import url_for

from . import valid_login_params, create_user


@pytest.fixture()
def sample_user():
    return {"name": "john doe", "email": "john@example.com", "password": "password"}


def test_login_page(client):
    response = client.get(url_for("auth.login"))

    assert response.status_code == 200
    assert b"Sign into your account" in response.data


def test_login(client, init_database, valid_login_params):
    create_user()
    response = client.post(
        url_for("auth.login"), data=valid_login_params, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_login_invalid_credentials(client, init_database, valid_login_params):
    create_user()
    invalid_data = valid_login_params.copy()
    invalid_data["password"] = "wrong password"

    response = client.post(
        url_for("auth.login"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_missing_email_error(client, init_database, valid_login_params):
    create_user()
    invalid_data = valid_login_params.copy()
    invalid_data["email"] = ""

    response = client.post(
        url_for("auth.login"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Email address cannot be empty" in response.data


def test_login_invalid_email_error(client, init_database, valid_login_params):
    create_user()
    invalid_data = valid_login_params.copy()
    invalid_data["email"] = "test@example"

    response = client.post(
        url_for("auth.login"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Please enter a valid email address" in response.data


def test_login_missing_password_error(client, init_database, valid_login_params):
    create_user()
    invalid_data = valid_login_params.copy()
    invalid_data["password"] = ""

    response = client.post(
        url_for("auth.login"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Password cannot be empty" in response.data


def test_login_already_logged_in_user(client, init_database, authenticated_request):
    response = client.get(url_for("auth.login"), follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data
