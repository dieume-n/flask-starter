from flask import url_for


def test_logout(client, init_database, authenticated_request):
    response = client.get(url_for("auth.logout"), follow_redirects=True)

    assert response.status_code == 200
    assert b"Sign into your account" in response.data


def test_logout_unauthenticated_user(client, init_database):
    response = client.get(url_for("auth.logout"), follow_redirects=True)

    assert response.status_code == 401
    # assert b"Sign into your account" in response.data