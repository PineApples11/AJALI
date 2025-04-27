
from Models.extensions import db
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request
)
from Models.models import User, Admin, IncidentReport, Media, TokenBlocklist
from datetime import datetime
import json
from functools import wraps




api = Blueprint('api', __name__)


def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if identity.get("role") != required_role:
                return jsonify({"error": "Unauthorized access"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

user_required = role_required("user")
admin_required = role_required("admin")


@api.route('/')
def index():
    return jsonify({"message": "Welcome to the AJALI API"}), 200


# --- AUTH ROUTES ---
@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_pw, phone_number=phone_number)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity={"id": new_user.id, "role": "user"})
    return jsonify(access_token=access_token, user={"id": new_user.id, "username": new_user.username}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": "user"})
    return jsonify(access_token=access_token, user={"id": user.id, "username": user.username}), 200


@api.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.utcnow()))
    db.session.commit()
    return jsonify(msg="Successfully logged out"), 200


# --- INCIDENT ROUTES ---
@api.route('/incidents', methods=['GET'])
@jwt_required()
@user_required
def get_incidents():
    reports = IncidentReport.query.all()
    return jsonify([{
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "type": r.type,
        "status": r.status,
        "longitude": r.longitude,
        "latitude": r.latitude,
        "user": r.user.username,
        "last_updated_by_admin": r.last_updated_by_admin.username if r.last_updated_by_admin else None
    } for r in reports]), 200


@api.route('/incidents', methods=['POST'])
@jwt_required()
@user_required
def create_incident():
    data = request.get_json()
    current_user = get_jwt_identity()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({"message": "Latitude and Longitude are required!"}),400

    incident = IncidentReport(
        title=data['title'],
        description=data['description'],
        type=data['type'],
        status='draft',
        longitude=data,
        latitude=data,
        user_id=current_user["id"]
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify({"message": "Incident created", "id": incident.id}), 201


@api.route('/incidents/<int:id>', methods=['GET'])
@jwt_required()
@user_required
def get_single_incident(id):
    incident = IncidentReport.query.get_or_404(id)
    return jsonify({
        "id": incident.id,
        "title": incident.title,
        "description": incident.description,
        "status": incident.status,
        "longitude": incident.longitude,
        "latitude": incident.latitude,
        "type": incident.type,
        "user": incident.user.username,
        "last_updated_by_admin": incident.last_updated_by_admin.username if incident.last_updated_by_admin else None
    }), 200


@api.route('/incidents/<int:id>', methods=['PATCH'])
@jwt_required()
@user_required
def update_incident(id):
    incident = IncidentReport.query.get_or_404(id)
    data = request.get_json()
    for field in ['title', 'description', 'longitude', 'latitude', 'type']:
        if field in data:
            setattr(incident, field, data[field])
    db.session.commit()
    return jsonify({"message": f"Incident {id} updated"}), 200


@api.route('/incidents/<int:id>', methods=['DELETE'])
@jwt_required()
@user_required
def delete_incident(id):
    incident = IncidentReport.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({"message": f"Incident {id} deleted"}), 204


# --- MEDIA ROUTES ---
@api.route('/incidents/<int:id>/media', methods=['POST'])
@jwt_required()
@user_required
def upload_media(id):
    incident = IncidentReport.query.get_or_404(id)
    data = request.get_json()
    image_urls = data.get('image_url', [])
    video_urls = data.get('video_url', [])

    if not isinstance(image_urls, list):
        image_urls = [image_urls]
    if not isinstance(video_urls, list):
        video_urls = [video_urls]

    media = Media(
        image_url=json.dumps(image_urls),
        video_url=json.dumps(video_urls),
        incident_reports_id=id
    )
    db.session.add(media)
    db.session.commit()
    return jsonify({"message": "Media uploaded successfully"}), 201


@api.route('/incidents/<int:id>/media', methods=['GET'])
@jwt_required()
@user_required
def get_media(id):
    media = Media.query.filter_by(incident_reports_id=id).all()
    return jsonify([{
        "id": m.id,
        "image_url": json.loads(m.image_url or "[]"),
        "video_url": json.loads(m.video_url or "[]"),
    } for m in media]), 200


# --- ADMIN ROUTES ---
@api.route('/admin/update_status/<int:id>', methods=['PATCH'])
@jwt_required()
@admin_required
def update_status(id):
    data = request.get_json()
    new_status = data.get('status')
    incident = IncidentReport.query.get_or_404(id)
    current_admin = get_jwt_identity()
    incident.status = new_status
    incident.last_updated_by_admin_id = current_admin["id"]
    db.session.commit()
    return jsonify({"message": f"Status for incident {id} updated to {new_status}"}), 200


# --- ADMIN AUTH ROUTES ---
@api.route('/admin/signup', methods=['POST'])
def admin_signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Admin already exists"}), 409

    hashed_pw = generate_password_hash(password)
    new_admin = Admin(username=username, email=email, password_hash=hashed_pw)

    db.session.add(new_admin)
    db.session.commit()

    access_token = create_access_token(identity={"id": new_admin.id, "role": "admin"})
    return jsonify(access_token=access_token, admin={"id": new_admin.id, "username": new_admin.username}), 201


@api.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()
    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({"error": "Invalid admin credentials"}), 401

    access_token = create_access_token(identity={"id": admin.id, "role": "admin"})
    return jsonify(access_token=access_token, admin={"id": admin.id, "username": admin.username}), 200