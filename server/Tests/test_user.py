from Models.models import User
from Models.extensions import db
import pytest

def test_create_user(app, db):
    # Create a user instance
    user = User(username="reporter", email="user@example.com", phone_number="0712345678")
    print(f"Creating user with username: {user.username}")  # Before commit
    
    # Set password
    user.set_password("password123")
    
    # Add user to the session and commit
    db.session.add(user)
    db.session.commit()

    # Fetch the user back from the database
    fetched_user = User.query.first()
    print(f"Fetched user with username: {fetched_user.username}")  # After commit

    # Assertions to verify user properties
    assert fetched_user.username == "reporter"
    assert fetched_user.check_password("password123") is True
    assert fetched_user.phone_number == "0712345678"
