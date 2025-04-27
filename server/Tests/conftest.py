import pytest
from flask import Flask
from Models.app import create_app
from Models.extensions import db as _db

TEST_DATABASE_URI = "postgresql://pineapples:postgres@localhost/test_ajali"

@pytest.fixture(scope="session")
def app():
    """Create the app with the 'testing' configuration"""
    app = create_app('testing')  # Use your create_app function for testing config
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        _db.create_all()  # Create all tables in the test database
        yield app
        _db.session.remove()  # Clean up after tests
        _db.drop_all()  # Drop all tables after tests

@pytest.fixture(scope="function", autouse=True)
def session(app, db):
    """ Rolls back after each test to ensure clean test isolation. """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    
    # Using db.session to manage the session in each test
    yield db.session

    transaction.rollback()  # Rollback to isolate tests
    connection.close()  # Close the connection after the test

@pytest.fixture
def client(app):
    """Provide a test client"""
    return app.test_client()

@pytest.fixture
def db(app):
    """Return the database object for tests"""
    return _db
