from flask_sqlalchemy import SQLAlchemy
from sql_serializer import serializerMixin # type: ignore
from app import bcrypt
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
metadata = MetaData ()

db = SQLAlchemy(metadata=metadata)


class Admin(db.Model,serializerMixin):
    __tablename__ = 'admins'
    serializer_rules = ('-password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    @validates('email')
    def validates_email(self,_,address):
        if'@' not in address:
            raise ValueError("Invalid email address")
        return address
    
    def set_password(self,password):
        self.password_hash=bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"<Admin {self.password_hash}>"


class User(db.Model,serializerMixin):
    __tablename__ = 'users'
    serializer_rules = ('-password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    incident_reports = db.relationship('IncidentReport', backref='user', lazy=True)
    
    @validates('email')
    def validates_email(self,_,address):
        if'@' not in address:
            raise ValueError("Invalid email address")
        return address
    
    def set_password(self,password):
        self.password_hash=bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"<User {self.username}>"

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

    def __repr__(self):
        return f"<IncidentReport {self.title}>"


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(256)) 
    Video_url = db.Column(db.String(256)) 
    incident_reports_id = db.Column(db.Integer, db.ForeignKey('incident_reports.id'), nullable=False)




class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)