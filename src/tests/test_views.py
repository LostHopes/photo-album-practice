def test_login_page(client):
    response = client.get("/login/")
    assert "Email" in response.get_data(as_text=True)
    assert "Password" in response.get_data(as_text=True)
    assert response.status_code == 200


def test_register_page(client):
    response = client.get("/register/")
    assert "Username" in response.get_data(as_text=True)
    assert "Email" in response.get_data(as_text=True)
    assert "Password" in response.get_data(as_text=True)
    assert response.status_code == 200


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
