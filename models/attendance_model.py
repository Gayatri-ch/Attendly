from utils.database import get_db_connection

class AttendanceModel:
    @staticmethod
    def mark_attendance(student_id, subject_id, status, date, time):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                INSERT IGNORE INTO attendance (student_id, subject_id, status, attendance_date, attendance_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, subject_id, status, date, time))
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                conn.commit()
            return rows_affected > 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_recent_activity(faculty_id, limit=5):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT a.attendance_date, a.attendance_time, s.subject_name, s.id as subject_id, COUNT(*) as present_count
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE s.faculty_id = %s
                GROUP BY a.attendance_date, a.attendance_time, s.subject_name, s.id
                ORDER BY a.attendance_date DESC, a.attendance_time DESC
                LIMIT %s
            """, (faculty_id, limit))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_attendance_history(student_id, limit=10):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT a.attendance_date, a.attendance_time, a.status, s.subject_name
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.id
                WHERE a.student_id = %s
                ORDER BY a.attendance_date DESC, a.attendance_time DESC
                LIMIT %s
            """, (student_id, limit))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_subject_attendance_stats(student_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT s.id, s.subject_name, s.subject_code,
                       (SELECT COUNT(*) FROM attendance a WHERE a.student_id = e.student_id AND a.subject_id = s.id AND a.status = 'Present') as present_count,
                       (SELECT COUNT(DISTINCT attendance_date) FROM attendance a WHERE a.subject_id = s.id) as total_days
                FROM enrollment e
                JOIN subjects s ON e.subject_id = s.id
                WHERE e.student_id = %s
            """, (student_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_detailed_attendance(student_id, subject_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT id, attendance_date, attendance_time, status
                FROM attendance
                WHERE student_id = %s AND subject_id = %s
                ORDER BY attendance_date DESC
            """, (student_id, subject_id))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def raise_flag(student_id, subject_id, attendance_id, reason):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                INSERT INTO attendance_reports (student_id, subject_id, attendance_id, reason)
                VALUES (%s, %s, %s, %s)
            """, (student_id, subject_id, attendance_id, reason))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_pending_reports(faculty_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT r.*, s.name as student_name, sub.subject_name, a.attendance_date
                FROM attendance_reports r
                JOIN students s ON r.student_id = s.id
                JOIN subjects sub ON r.subject_id = sub.id
                JOIN attendance a ON r.attendance_id = a.id
                WHERE sub.faculty_id = %s AND r.status = 'Pending'
            """, (faculty_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def resolve_report(report_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("UPDATE attendance_reports SET status='Resolved' WHERE id=%s", (report_id,))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_report_records(subject_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT s.student_uid, s.name, a.attendance_date, a.attendance_time, a.status
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                WHERE a.subject_id = %s
                ORDER BY a.attendance_date DESC, s.student_uid ASC
            """, (subject_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_audit_log(student_id, subject_id, confidence, status, event_type='AI_RECOGNITION'):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                INSERT INTO attendance_audit_logs (student_id, subject_id, recognition_confidence, attendance_status, event_type)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, subject_id, confidence, status, event_type))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()
