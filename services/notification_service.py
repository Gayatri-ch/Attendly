class NotificationService:
    @staticmethod
    def notify_low_attendance(student_id, subject_id, percentage):
        print(f"[NOTIFICATION] Student {student_id} has low attendance in {subject_id}: {percentage}%")
        # In a real app, this would send an email or push notification

    @staticmethod
    def notify_discrepancy_raised(faculty_id, report_id):
        print(f"[NOTIFICATION] Faculty {faculty_id} has a new discrepancy report: {report_id}")
