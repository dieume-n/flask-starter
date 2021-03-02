from flask import url_for
from app.users.models import User

from . import valid_register_params


def test_register_page(client):
    response = client.get(url_for("auth.register"))

    assert response.status_code == 200
    assert "Sign up with us" in str(response.data)


def test_register(client, init_database, valid_register_params):
    response = client.post(
        url_for("auth.register"), data=valid_register_params, follow_redirects=True
    )
    user = User.find_by_email(valid_register_params["email"])

    assert response.status_code == 200
    assert "please login" in str(response.data)
    assert user.name == valid_register_params["name"].title()
    assert user.email == valid_register_params["email"]


def test_register_missing_name_error(client, init_database, valid_register_params):
    invalid_data = valid_register_params.copy()
    invalid_data["name"] = ""
    response = client.post(
        url_for("auth.register"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert User.query.count() == 0
    assert b"Name cannot be empty" in response.data


def test_register_invalid_name_error(client, init_database, valid_register_params):
    invalid_data = valid_register_params.copy()
    invalid_data["name"] = "ab"
    response = client.post(
        url_for("auth.register"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert User.query.count() == 0
    assert b"Name must be atleast 3 characters long" in response.data


def test_register_missing_email_error(client, init_database, valid_register_params):
    invalid_data = valid_register_params.copy()
    invalid_data["email"] = ""
    response = client.post(
        url_for("auth.register"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert User.query.count() == 0
    assert b"Email address cannot be empty" in response.data


def test_register_invalid_email_error(client, init_database, valid_register_params):
    invalid_data = valid_register_params.copy()
    invalid_data["email"] = "ab@example"
    response = client.post(
        url_for("auth.register"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert User.query.count() == 0
    assert b"Please enter a valid email address" in response.data


def test_register_missing_password_error(client, init_database, valid_register_params):
    invalid_data = valid_register_params.copy()
    invalid_data["password"] = ""
    response = client.post(
        url_for("auth.register"), data=invalid_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert User.query.count() == 0
    assert b"Password cannot be empty" in response.data


def test_register_already_logged_in_user(client, init_database, authenticated_request):
    response = client.get(url_for("auth.register"), follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_register_existing_user(
    client, init_database, create_user, valid_register_params
):
    response = client.post(
        url_for("auth.register"), data=valid_register_params, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Sorry! this email is already taken." in response.data
