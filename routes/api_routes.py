from flask import Blueprint, jsonify, request, session
from utils.security import login_required
from services.analytics_service import AnalyticsService
from models.subject_model import SubjectModel
import subprocess

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/student/attendance")
@login_required(role="student")
def get_student_attendance():
    student_id = session["user"]["id"]
    subjects, _ = AnalyticsService.get_student_dashboard_data(student_id)
    return jsonify(subjects)

@api_bp.route("/faculty/subjects")
@login_required(role="faculty")
def get_faculty_subjects():
    faculty_id = session["user"]["id"]
    subjects = SubjectModel.get_subjects_by_faculty(faculty_id)
    return jsonify(subjects)

@api_bp.route("/attendance/start", methods=["POST"])
@login_required(role="faculty")
def start_attendance():
    data = request.json
    subject_id = data.get("subject_id")
    subject_name = data.get("subject_name")

    if not subject_id or not subject_name:
        return jsonify({"error": "Missing subject info"}), 400

    try:
        subprocess.Popen([
            "python", "attendance.py",
            "-s", str(subject_id),
            "-sn", subject_name,
            "-f", session["user"]["name"]
        ])
        return jsonify({"status": "started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
