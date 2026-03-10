CREATE DATABASE IF NOT EXISTS attendly_db;
USE attendly_db;

-- Disable foreign key checks for clean drop
SET FOREIGN_KEY_CHECKS = 0;

-- Drop all possible existing tables to ensure schema consistency
DROP TABLE IF EXISTS attendance_audit_logs;
DROP TABLE IF EXISTS attendance_reports;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS attendance_records; -- legacy name
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS enrollments; -- legacy name
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS classes; -- legacy name
DROP TABLE IF EXISTS courses; -- legacy name
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS faculty;

-- Re-enable checks
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Faculty Table
CREATE TABLE faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_uid VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Students Table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_uid VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Subjects Table
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE,
    INDEX (faculty_id)
);

-- 4. Enrollment Table
CREATE TABLE enrollment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    UNIQUE(student_id, subject_id)
);

-- 5. Attendance Table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    status ENUM('Present', 'Absent') DEFAULT 'Present',
    attendance_date DATE NOT NULL,
    attendance_time TIME NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    INDEX (attendance_date),
    INDEX (student_id, subject_id),
    UNIQUE(student_id, subject_id, attendance_date)
);

-- 6. Attendance Reports Table
CREATE TABLE attendance_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    attendance_id INT NOT NULL,
    reason TEXT NOT NULL,
    status ENUM('Pending', 'Resolved') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (attendance_id) REFERENCES attendance(id) ON DELETE CASCADE
);

-- 7. Attendance Audit Logs Table (New for refactor)
CREATE TABLE attendance_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    recognition_confidence FLOAT,
    attendance_status VARCHAR(20), -- e.g., 'Present', 'Absent', 'Flagged'
    event_type ENUM('AI_RECOGNITION', 'MANUAL_MARK', 'REPORT_RESOLVED') DEFAULT 'AI_RECOGNITION',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);
