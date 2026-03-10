# Attendly - Smart Attendance System (Modular Edition)

Attendly is a modern, AI-powered Smart Attendance System built with **Flask (Python)**, **MySQL**, and **Computer Vision**. This version has been fully refactored into a modular, service-oriented architecture for production-like scalability.

##  Features

### **For Faculty (Teachers)**
- **Modular Dashboard**: Real-time stats, recent activity, and student discrepancy reports.
- **Subject Management**: Create subjects and enroll students using the `SubjectModel`.
- **AI Attendance Session**: Trigger face recognition sessions using the `FaceRecognitionService`.
- **Attendance Auditing**: Automatic logging of recognition events with confidence scores.
- **Manual Resolution**: Review and resolve fishy attendance flags.

### **For Students**
- **Personalized Analytics**: View attendance trends and percentages using the `AnalyticsService`.
- **History View**: Day-by-day attendance logs with status indicators.
- **Report Discrepancies**: Flag incorrect attendance marks directly on the dashboard.

##  Architecture
The project follows a clean **Separation of Concerns**:

- `models/`: Data access layer for Students, Faculty, Subjects, and Attendance.
- `services/`: Core business logic (Face Recognition, Analytics, Attendance, Notifications).
- `routes/`: Modular endpoints using Flask Blueprints (`auth`, `faculty`, `student`, `api`).
- `utils/`: Shared utilities for database connections and security.
- `config.py`: Centralized configuration management.

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: MySQL
- **AI Engine**: DeepFace (Facenet512, RetinaFace)
- **Frontend**: HTML5, CSS3, JavaScript
- **Analytics**: Chart.js

## Installation

### 1. Prerequisites
- Python 3.8+
- MySQL Server

### 2. Setup
```bash
git clone https://github.com/Gayatri-ch/smartattendancesys.git
cd smartattendancesys
pip install -r requirements.txt
```

### 3. Database Initialization
1. Create a MySQL database named `attendly_db`.
2. Update `config.py` with your database credentials.
3. Import the schema:
```sql
mysql -u root -p attendly_db < setup_db.sql
```

### 4. Run the Application
```bash
python app.py
```
Visit `http://localhost:5001`.

## Security
- **Password Hashing**: PBKDF2 with SHA256.
- **Role-Based Access**: Enforced via `@login_required` decorators in `utils/security.py`.

## Screenshots
<img width="1879" height="838" alt="Screenshot 2026-03-10 140956" src="https://github.com/user-attachments/assets/df774b01-4f05-4269-b651-961311b58f1d" />
<img width="1852" height="836" alt="Screenshot 2026-03-10 140945" src="https://github.com/user-attachments/assets/2d9394d6-483c-4c8b-8b2f-6f9bd87e7bae" />
<img width="1861" height="863" alt="Screenshot 2026-03-10 140935" src="https://github.com/user-attachments/assets/7d51bf8b-38a6-4685-a312-987cdfc10fc9" />
<img width="1890" height="848" alt="Screenshot 2026-03-10 140910" src="https://github.com/user-attachments/assets/553e2c5b-9314-4031-a8cd-6f59aea27424" />
<img width="1874" height="856" alt="Screenshot 2026-03-10 140858" src="https://github.com/user-attachments/assets/deac718e-10a3-4291-92cd-7ac647acc38f" />
<img width="1876" height="851" alt="Screenshot 2026-03-10 140846" src="https://github.com/user-attachments/assets/0f995b4c-125e-4f6e-a35b-1eda78ca230c" />
