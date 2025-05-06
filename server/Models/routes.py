# app/routes.py
from flask import Blueprint, jsonify
from .models import db, IncidentReport

bp = Blueprint('main', __name__)

@bp.route('/api/reports', methods=['GET'])
def get_reports():
    reports = IncidentReport.query.all()
    reports_data = []
    for report in reports:
        reports_data.append({
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'type': report.type,
            'status': report.status,
            'longitude': report.longitude,
            'latitude': report.latitude,
            'timestamp': report.created_at,
        })
    return jsonify(reports_data)
