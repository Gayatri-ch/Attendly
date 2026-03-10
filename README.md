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