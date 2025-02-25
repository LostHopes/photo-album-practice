from app.models import User
from app import db


def test_create_user(client):
    with client.application.app_context():
        username = "TestUser123"
        email = "test@gmail.com"
        password = "password"
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        assert user.is_authenticated
        assert user.is_active
        assert not user.is_anonymous
        assert User.query.count() == 1


def test_get_user(client):
    with client.application.app_context():
        user = db.session.query(User).first()
    
    assert user.id == 1
    assert user.username == "TestUser123"


def test_update_user(client):
    with client.application.app_context():
        user = User.query.first()
        user.email = "altered@gmail.com"
        db.session.add(user)
        db.session.commit()

        user = db.session.query(User).first()
        assert user.email == "altered@gmail.com"


def test_delete_user(client):
    with client.application.app_context():
        username = "TestUser123"
        user = db.session.query(User).first()
        db.session.delete(user)
        db.session.commit()

        assert User.query.count() == 0
