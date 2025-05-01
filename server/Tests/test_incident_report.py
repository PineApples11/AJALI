from Models.extensions import db
from Models.models import User, IncidentReport, IncidentTypeEnum, IncidentStatusEnum

def test_create_incident_report(db):
    user = User(username="reporter", email="reporter@example.com", phone_number="0799999999")
    user.set_password("reportpass")
    db.session.add(user)
    db.session.commit()

    incident = IncidentReport(
        title="Road Accident",
        description="Major accident at highway",
        type=IncidentTypeEnum.RED_FLAG,
        status=IncidentStatusEnum.DRAFT,
        longitude=36.8219,
        latitude=-1.2921,
        user_id=user.id
    )
    db.session.add(incident)
    db.session.commit()

    fetched_incident = IncidentReport.query.first()
    assert fetched_incident.title == "Road Accident"
    assert fetched_incident.user.username == "reporter"
