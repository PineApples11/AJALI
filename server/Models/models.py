from flask_sqlalchemy import SQLAlchemy
 from sql_serializer import serializerMixin # type: ignore
 from sqlalchemy import MetaData
 metadata = MetaData ()
 
 db = SQLAlchemy(metadata=metadata)
 
 
 class Admin(db.Model):
     __tablename__ = 'admins'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(128), nullable=False)
     email = db.Column(db.String(120), nullable=False)
     password_hash = db.Column(db.String(128), nullable=False)
 
 class User(db.Model,serializerMixin):
     serializer_rules = ('-password_hash','-incident-user',)
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(128), nullable=False)
     email = db.Column(db.String(120), nullable=False)
     password_hash = db.Column(db.String(128), nullable=False)
     phone_number = db.Column(db.String(20), nullable=False)
 
     incident_reports = db.relationship('IncidentReport', backref='user', lazy=True)
 
 
 class IncidentReport(db.Model):
     __tablename__ = 'incident_reports'
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(128), nullable=False)
     description = db.Column(db.String(256), nullable=False)
     type = db.Column(db.Enum('red-flag', 'intervention', name='incident_type'), nullable=False)
     status = db.Column(db.Enum('draft','under_investigation', 'resolved','rejected', name='incident_status'), default='draft')
     longitude = db.Column(db.Float, nullable=False)
     latitude = db.Column(db.Float, nullable=False)
    
 
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
     last_updated_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
     last_updated_by_admin = db.relationship('Admin', backref='updated_reports', lazy=True)
     media = db.relationship('Media', backref='incident_report', lazy=True)
 
 
 class Media(db.Model):
     __tablename__ = 'media'
     id = db.Column(db.Integer, primary_key=True)
     image_url = db.Column(JSON)
     Video_url = db.Column(JSON)
     incident_reports_id = db.Column(db.Integer, db.ForeignKey('incident_reports.id'), nullable=False)
 
 
 
 
 class TokenBlocklist(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     jti = db.Column(db.String(36), nullable=False, index=True)
     created_at = db.Column(db.DateTime, nullable=False)