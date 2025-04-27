from Models.extensions import db
from Models.models import User

def test_create_user(db):
    user = User(username="user1", email="user@example.com", phone_number="0712345678")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.first()
    assert fetched_user.username == "user1"
    assert fetched_user.check_password("password123") is True
    assert fetched_user.phone_number == "0712345678"
