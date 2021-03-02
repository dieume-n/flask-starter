import pytest
from app.users.models import User

EXAMPLE_EMAIL = "john@example.com"
EXAMPLE_NAME = "john doe"
EXAMPLE_PASSWORD = "testing101"

# VALID_REGISTER_PARAMS = {
#     "name": EXAMPLE_NAME,
#     "email": EXAMPLE_EMAIL,
#     "password": EXAMPLE_PASSWORD,
# }

# VALID_LOGIN_PARAMS = {"email": EXAMPLE_EMAIL, "password": EXAMPLE_PASSWORD}


@pytest.fixture(scope="module")
def valid_register_params():
    return {
        "name": EXAMPLE_NAME,
        "email": EXAMPLE_EMAIL,
        "password": EXAMPLE_PASSWORD,
    }


@pytest.fixture(scope="module")
def valid_login_params():
    return {
        "email": EXAMPLE_EMAIL,
        "password": EXAMPLE_PASSWORD,
    }


def create_user():
    user = User(name=EXAMPLE_NAME, email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD)
    user.save()
    return user
