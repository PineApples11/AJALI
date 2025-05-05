import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.app import create_app
from Models.extensions import db
from Models.models import User, Admin, Media, IncidentReport
from faker import Faker
import random

fake=Faker()
app = create_app()

with app.app_context():

  print("Clearing existing data...")
  Media.query.delete()
  IncidentReport.query.delete()
  User.query.delete()
  # Admin.query.delete()

  # cleans the db if existing data iko
 
  print("Seeding admins...")
  admins = []

  for _ in range(5):
      admin = Admin(
          username=fake.user_name(),
          email=fake.email(),
      )

      admin.set_password("password")
      admins.append(admin)
      db.session.add(admin)

  db.session.commit()

  print("Seeding users...")
  users = []

  for _ in range(25):
    user = User(
      username=fake.user_name(),
      email=fake.email(),
      phone_number=fake.phone_number(),

    )

    user.set_password("password")
    users.append(user)
    db.session.add(user)
  
  db.session.commit()

  print("Seeding incidents...")
  incidents = []
  for _ in range(25):
        incident = IncidentReport(
            title=fake.sentence(nb_words=6),
            description=fake.paragraph(nb_sentences=3),
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            user_id=random.choice(users).id,
            status=fake.random_element(elements=["DRAFT", "UNDER_INVESTIGATION", "RESOLVED", "REJECTED"]),
            type = fake.random_element(elements=["RED_FLAG", "INTERVENTION"]),
            # incident_type=random.choice(['Accident', 'Fire', 'Theft', 'Medical Emergency'])

        )
        incidents.append(incident)
        db.session.add(incident)
    
  db.session.commit()

  print("Seeding media...")
  for _ in range(25):
        media = Media(
            image_url=fake.image_url(),
            video_url=fake.url(),
            incident_reports_id=fake.random_element(elements=[incident.id for incident in incidents])
        )
        db.session.add(media)
    
  db.session.commit()


  # if not Admin.query.first():
  #   admin = Admin(username="admin",email="admin@ajali.com")
  #   admin.set_password("password123")
  #   db.session.add(admin)

  # if not User.query.first():
  #       user = User(username="john_doe", email="john@ajali.com", phone_number="0712345678")
  #       user.set_password("userpass123")
  #       db.session.add(user)

  
  db.session.commit()
  print("✅ Database seeded successfully!")