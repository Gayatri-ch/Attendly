import os
import cv2
import argparse
from datetime import datetime
import sys

# Add project root to path to ensure imports work when run as a script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from services.face_recognition_service import FaceRecognitionService
from services.attendance_service import AttendanceService
from models.user_model import UserModel

# ---------------- ARGUMENTS ----------------
def parse_args():
    parser = argparse.ArgumentParser(description="AI Face Recognition Attendance System")
    parser.add_argument("--dataset", "-d", default=Config.UPLOAD_FOLDER, help="Folder containing student images")
    parser.add_argument("--subject_id", "-s", required=True, help="Subject ID (DB Primary Key)")
    parser.add_argument("--subject_name", "-sn", required=True, help="Subject Name")
    parser.add_argument("--faculty", "-f", required=True, help="Faculty name")
    parser.add_argument("--camera-index", type=int, default=0, help="Webcam index")
    return parser.parse_args()

# ---------------- MAIN ----------------
def main():
    args = parse_args()

    if not os.path.exists(args.dataset):
        os.makedirs(args.dataset)

    print(f"[INFO] Subject: {args.subject_name} (ID: {args.subject_id}) | Faculty: {args.faculty}")
    print("[INFO] Initializing Face Recognition Model...")

    images = [f for f in os.listdir(args.dataset) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not images:
         print("[ERROR] No student images found. Please upload photos first.")
         return

    cap = cv2.VideoCapture(args.camera_index)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[INFO] Press 'q' to end attendance session.")
    banner = f"{args.subject_name} | {args.faculty}"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # UI Overlay
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (45, 45, 45), -1)
        cv2.putText(frame, banner, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 170), 2)

        # Use Face Recognition Service
        match = FaceRecognitionService.find_match(frame, args.dataset)

        if match is not None:
            filename = os.path.basename(match["identity"])
            if "_" in filename:
                uid = filename.split("_", 1)[0]
                student = UserModel.get_student_by_uid(uid)
                
                if student:
                    # Use Attendance Service to mark and audit
                    AttendanceService.mark_attendance(
                        student["id"], 
                        args.subject_id, 
                        status='Present', 
                        confidence=float(1.0 - match["distance"]) # Confidence calculation
                    )

                    label = f"Recognized: {uid}"
                    cv2.putText(frame, label, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Attendly Smart Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Session ended.")

if __name__ == "__main__":
    main()