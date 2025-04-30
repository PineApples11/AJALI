import pytest
from Models.app import create_app
from Models.extensions import db as _db

@pytest.fixture(scope="function")
def app():
    # Create the app instance for testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory database for testing
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # Create tables for testing
    with app.app_context():
        _db.create_all()
        yield app  # Yield the app for test functions to use
        _db.session.remove()
        _db.drop_all()  # Clean up the database after tests

@pytest.fixture(scope="function")
def db(app):
    # Return the database object to the test function
    return _db
