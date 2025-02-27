def test_register(client):
    response = client.post(
        "/register/",
        data={
            "username": "TestUser123",
            "email": "test@gmail.com",
            "password": "password",
            "confirm_password": "password",
            "accept_rules": True,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.request.path == "/login/"


def test_login(client):
    response = client.post(
        "/login/",
        data={"email": "test@gmail.com", "password": "password"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.request.path == "/albums/"
