from Models.extensions import db
from Models.models import User, IncidentReport, IncidentTypeEnum, IncidentStatusEnum, Media

def test_create_media(db):
    user = User(username="mediaperson", email="media@example.com", phone_number="0788888888")
    user.set_password("mediapass")
    db.session.add(user)
    db.session.commit()

    incident = IncidentReport(
        title="Fire Outbreak",
        description="Warehouse caught fire",
        type=IncidentTypeEnum.INTERVENTION,
        status=IncidentStatusEnum.UNDER_INVESTIGATION,
        longitude=36.8219,
        latitude=-1.2921,
        user_id=user.id
    )
    db.session.add(incident)
    db.session.commit()

    media = Media(
        image_url="https://example.com/image.jpg",
        video_url="https://example.com/video.mp4",
        incident_reports_id=incident.id
    )
    db.session.add(media)
    db.session.commit()

    fetched_media = Media.query.first()
    assert fetched_media.image_url == "https://example.com/image.jpg"
    assert fetched_media.incident_report.title == "Fire Outbreak"
