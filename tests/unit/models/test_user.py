from app.users.models import User
from app.extensions import bcrypt

user_dict = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secret",
}


def test_new_user(client, init_database):
    """
    GIVEN a User model
    WHEN a new user is created
    THEN check the name, email and hashed_password fields are defined correctly
    """
    user = User(**user_dict)
    user.save()

    registered_user = User.query.filter_by(name=user_dict["name"]).first_or_404()

    assert registered_user.name == user_dict["name"].title()
    assert registered_user.email == user_dict["email"].lower()
    assert True is bcrypt.check_password_hash(
        registered_user.password, user_dict["password"]
    )


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new user is created
    THEN check the name, email and hashed_password fields are defined correctly
    """
    assert new_user.email == user_dict["email"]
    assert new_user.name == user_dict["name"]


def test_setting_password(new_user):
    """
    GIVEN an existing user
    WHEN the password for the user is set
    THEN check the password is stored correctly and not in plain text
    """
    new_password = "MyNewPassword"
    new_user.set_password(new_password)
    # new_user.save()

    assert new_user.password != new_password
    assert new_user.check_password(new_password)
    assert not new_user.check_password("MyNewPassword2")