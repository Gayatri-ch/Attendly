from utils.database import get_db_connection

class SubjectModel:
    @staticmethod
    def get_subjects_by_faculty(faculty_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("SELECT * FROM subjects WHERE faculty_id=%s", (faculty_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_total_subjects_count(faculty_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM subjects WHERE faculty_id=%s", (faculty_id,))
            return cursor.fetchone()["count"]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_enrolled_subjects_by_student(student_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                SELECT s.* FROM enrollment e
                JOIN subjects s ON e.subject_id = s.id
                WHERE e.student_id = %s
            """, (student_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_subject(faculty_id, name, code, description):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("""
                INSERT INTO subjects (faculty_id, subject_name, subject_code, description)
                VALUES (%s, %s, %s, %s)
            """, (faculty_id, name, code, description))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def enroll_student(student_id, subject_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("INSERT INTO enrollment (student_id, subject_id) VALUES (%s, %s)", (student_id, subject_id))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_enrollment_count(subject_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM enrollment WHERE subject_id=%s", (subject_id,))
            return cursor.fetchone()["count"]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_subject_by_id(subject_id):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("SELECT * FROM subjects WHERE id=%s", (subject_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
