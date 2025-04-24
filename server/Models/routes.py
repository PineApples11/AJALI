
from flask import Blueprint, request, jsonify
from models import db, User, Admin, IncidentReport


# Initialize Blueprint
api = Blueprint('api', __name__)

# --- AUTH ROUTES ---
@api.route('/signup', methods=['POST'])
def signup():
    # Logic for user registration (2-step auth optional)
    return jsonify({"message": "Signup endpoint"}), 201

@api.route('/login', methods=['POST'])
def login():
    # Logic for JWT login
    return jsonify({"message": "Login endpoint"}), 200

# --- INCIDENT ROUTES ---
@api.route('/incident_reports', methods=['GET'])
def get_incidents():
    # Return paginated list of incident reports
    return jsonify({"message": "List incidents"}), 200

@api.route('/incident_reports', methods=['POST'])
def create_incident():
    # Logic to create an incident
    return jsonify({"message": "Incident created"}), 201

@api.route('/incident_reports/<int:id>', methods=['GET'])
def get_single_incident(id):
    # Logic to get one incident
    return jsonify({"message": f"Get incident {id}"}), 200

@api.route('/incident_reports/<int:id>', methods=['PATCH'])
def update_incident(id):
    # Logic to update an incident (title, location, etc.)
    return jsonify({"message": f"Incident {id} updated"}), 200

@api.route('/incident_reports/<int:id>', methods=['DELETE'])
def delete_incident(id):
    # Logic to delete incident
    return jsonify({"message": f"Incident {id} deleted"}), 204

# --- ADMIN ROUTES ---
@api.route('/admin/update_status/<int:id>', methods=['PATCH'])
def update_status(id):
    # Logic to change incident status
    return jsonify({"message": f"Status for incident {id} updated"}), 200
