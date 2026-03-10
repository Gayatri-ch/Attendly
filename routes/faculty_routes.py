from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from utils.security import login_required
from services.analytics_service import AnalyticsService
from models.subject_model import SubjectModel
from models.user_model import UserModel
from models.attendance_model import AttendanceModel
import os
import io
import csv
from config import Config

faculty_bp = Blueprint("faculty", __name__)

@faculty_bp.route("/tdashboard")
@login_required(role="faculty")
def dashboard():
    faculty_id = session["user"]["id"]
    subjects, total_subjects, total_students, recent_activity, pending_reports = AnalyticsService.get_faculty_dashboard_stats(faculty_id)
    
    return render_template("tdashboard.html", 
                           user=session["user"], 
                           subjects=subjects, 
                           total_subjects=total_subjects, 
                           total_students=total_students,
                           recent_activity=recent_activity,
                           pending_reports=pending_reports)

@faculty_bp.route("/resolve_report/<int:report_id>")
@login_required(role="faculty")
def resolve_report(report_id):
    if AttendanceModel.resolve_report(report_id):
        flash("Report marked as resolved.")
    return redirect(url_for("faculty.dashboard"))

@faculty_bp.route("/subjects")
@login_required(role="faculty")
def subjects():
    faculty_id = session["user"]["id"]
    subjects = SubjectModel.get_subjects_by_faculty(faculty_id)
    for subject in subjects:
        subject["enrolled_count"] = SubjectModel.get_enrollment_count(subject["id"])
    
    return render_template("subjects.html", user=session["user"], subjects=subjects)

@faculty_bp.route("/add_subject", methods=["POST"])
@login_required(role="faculty")
def add_subject():
    sname = request.form["subject_name"]
    scode = request.form["subject_code"]
    desc = request.form.get("description", "")
    fid = session["user"]["id"]

    if SubjectModel.create_subject(fid, sname, scode, desc):
        flash("Subject added successfully!")
    else:
        flash("Subject code already exists!")
    return redirect(url_for("faculty.subjects"))

@faculty_bp.route("/enroll", methods=["POST"])
@login_required(role="faculty")
def enroll():
    suid = request.form["student_uid"]
    sid = request.form["subject_id"]

    student = UserModel.get_student_by_uid(suid)
    if not student:
        flash("Student not found!")
        return redirect(url_for("faculty.subjects"))

    if SubjectModel.enroll_student(student["id"], sid):
        flash("Student enrolled successfully!")
    else:
        flash("Student already enrolled in this subject!")
    return redirect(url_for("faculty.subjects"))

@faculty_bp.route("/upload_photo", methods=["GET", "POST"])
@login_required(role="faculty")
def upload_photo():
    if request.method == "POST":
        uid = request.form["student_uid"]
        file = request.files["photo"]
        
        if file:
            student = UserModel.get_student_by_uid(uid)
            if student:
                filename = f"{uid}_{student['name'].replace(' ', '_')}.jpg"
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(filepath)
                UserModel.update_photo_path(uid, filepath)
                flash(f"Photo uploaded successfully for {student['name']}!")
            else:
                flash("Student UID not found!")
            return redirect(url_for("faculty.dashboard"))

    faculty_id = session["user"]["id"]
    subjects = SubjectModel.get_subjects_by_faculty(faculty_id)
    return render_template("uploadphoto.html", user=session["user"], subjects=subjects)

@faculty_bp.route("/download_report/<int:subject_id>")
@login_required(role="faculty")
def download_report(subject_id):
    records = AttendanceModel.get_report_records(subject_id)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student UID", "Name", "Date", "Time", "Status"])
    for row in records:
        writer.writerow([row["student_uid"], row["name"], row["attendance_date"], row["attendance_time"], row["status"]])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"attendance_report_{subject_id}.csv"
    )
