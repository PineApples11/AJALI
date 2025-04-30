from Models.extensions import db
from Models.models import Admin

def test_create_admin(db):
    admin = Admin(username="admin1", email="admin@example.com")
    admin.set_password("securepassword")
    db.session.add(admin)
    db.session.commit()

    fetched_admin = Admin.query.first()
    assert fetched_admin.username == "admin1"
    assert fetched_admin.check_password("securepassword") is True
