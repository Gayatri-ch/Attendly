from models.attendance_model import AttendanceModel
from datetime import datetime

class AttendanceService:
    @staticmethod
    def mark_attendance(student_id, subject_id, status='Present', confidence=None):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        marked = AttendanceModel.mark_attendance(student_id, subject_id, status, date_str, time_str)
        
        if marked:
            # Audit the event
            AttendanceModel.add_audit_log(
                student_id, 
                subject_id, 
                confidence, 
                status, 
                'AI_RECOGNITION' if confidence else 'MANUAL_MARK'
            )
        return marked
