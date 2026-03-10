from models.attendance_model import AttendanceModel
from models.subject_model import SubjectModel

class AnalyticsService:
    @staticmethod
    def get_student_dashboard_data(student_id):
        subjects = AttendanceModel.get_subject_attendance_stats(student_id)
        for s in subjects:
            if s["total_days"] > 0:
                s["percentage"] = round((s["present_count"] / s["total_days"]) * 100, 2)
            else:
                s["percentage"] = 0
        
        history = AttendanceModel.get_attendance_history(student_id)
        return subjects, history

    @staticmethod
    def get_faculty_dashboard_stats(faculty_id):
        total_subjects = SubjectModel.get_total_subjects_count(faculty_id)
        
        subjects = SubjectModel.get_subjects_by_faculty(faculty_id)
        total_students = sum(SubjectModel.get_enrollment_count(s["id"]) for s in subjects)
        
        recent_activity = AttendanceModel.get_recent_activity(faculty_id)
        pending_reports = AttendanceModel.get_pending_reports(faculty_id)
        
        return subjects, total_subjects, total_students, recent_activity, pending_reports
