from flask_login import login_user
from app.user.models import User
from app import db


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


def test_albums_page(client):
    response = client.get("/albums/", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login/"


def test_empty_album_page(client):
    response = client.get("/albums/1/", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login/"
