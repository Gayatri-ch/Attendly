from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.security import login_required
from services.analytics_service import AnalyticsService
from models.subject_model import SubjectModel
from models.attendance_model import AttendanceModel

student_bp = Blueprint("student", __name__)

@student_bp.route("/sdashboard")
@login_required(role="student")
def dashboard():
    student_id = session["user"]["id"]
    subjects, history = AnalyticsService.get_student_dashboard_data(student_id)
    
    return render_template("sdashboard.html", user=session["user"], subjects=subjects, history=history)

@student_bp.route("/subject_attendance/<int:subject_id>")
@login_required(role="student")
def subject_attendance(subject_id):
    student_id = session["user"]["id"]
    
    subjects = SubjectModel.get_enrolled_subjects_by_student(student_id)
    subject = SubjectModel.get_subject_by_id(subject_id)
    records = AttendanceModel.get_detailed_attendance(student_id, subject_id)

    return render_template("subject_attendance.html", user=session["user"], subject=subject, records=records, subjects=subjects)

@student_bp.route("/report_attendance", methods=["POST"])
@login_required(role="student")
def report_attendance():
    attendance_id = request.form["attendance_id"]
    subject_id = request.form["subject_id"]
    reason = request.form["reason"]
    student_id = session["user"]["id"]

    if AttendanceModel.raise_flag(student_id, subject_id, attendance_id, reason):
        flash("Flag raised! Your teacher will review it.")
    else:
        flash("You have already reported this record.")
    
    return redirect(url_for("student.subject_attendance", subject_id=subject_id))
