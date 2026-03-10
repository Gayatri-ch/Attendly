from utils.database import get_db_connection

class UserModel:
    @staticmethod
    def get_user_by_uid(uid, role):
        conn, cursor = get_db_connection()
        try:
            table = "faculty" if role == "faculty" else "students"
            uid_col = "faculty_uid" if role == "faculty" else "student_uid"
            cursor.execute(f"SELECT * FROM {table} WHERE {uid_col}=%s", (uid,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_user(uid, name, email, password, role):
        conn, cursor = get_db_connection()
        try:
            if role == "student":
                cursor.execute("""
                    INSERT INTO students (student_uid, name, email, password)
                    VALUES (%s, %s, %s, %s)
                """, (uid, name, email, password))
            else:
                cursor.execute("""
                    INSERT INTO faculty (faculty_uid, name, email, password)
                    VALUES (%s, %s, %s, %s)
                """, (uid, name, email, password))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_photo_path(uid, photo_path):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("UPDATE students SET photo_path=%s WHERE student_uid=%s", (photo_path, uid))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_student_by_uid(uid):
        conn, cursor = get_db_connection()
        try:
            cursor.execute("SELECT id, name FROM students WHERE student_uid=%s", (uid,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
