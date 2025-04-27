import pytest
from app import create_app
from Models.extensions import db as _db
from sqlalchemy import text

TEST_DATABASE_URI = "postgresql://your_user:your_password@localhost/your_test_database"

@pytest.fixture(scope="session")
def app():
    app = create_app('testing')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.close()
        # Drop all tables after tests to keep it clean
        _db.drop_all()

@pytest.fixture(scope="function", autouse=True)
def session(db):
    """Rolls back after each test for clean isolation."""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    sess = db.create_scoped_session(options=options)

    db.session = sess

    yield sess

    transaction.rollback()
    connection.close()
    sess.remove()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db
