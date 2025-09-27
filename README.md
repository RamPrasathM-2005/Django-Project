# 🎉 Workshop Management System

A **Django-based web application** designed to manage workshops with features like **student enrollment, attendance tracking, certificate generation, and analytics**.  
This project demonstrates contributions from three team members, each responsible for specific modules.

---

## 🚀 Features

### 👤 Member 1: Workshop Listing & Enrollment

- **Workshop Model**: Defines workshops with `title`, `description`, `date`, `capacity`, and `created_at`.
- **Enrollment Model**: Manages student enrollments (ensures a student can enroll only once per workshop).
- **Workshop Listing View**: Lists all workshops (`workshops.html`), ordered by date.
- **Admin Interface**: Manage workshops & enrollments with search/filter support.

### 📝 Member 2: Attendance Tracking

- **Attendance Model**: Tracks student attendance with `student`, `workshop`, `date`, and `present`.
- **Unique Constraint**: Ensures one attendance record per student per workshop per date.
- **Admin Interface**: Record and filter attendance by workshop, date, and status.

### 📜 Member 3: Certificate Generation & Analytics

- **Certificate Model**: Stores `student`, `workshop`, `issued_date`, and `pdf`. Prevents duplicates.
- **Certificate Generation**: Uses **ReportLab** to generate a downloadable PDF certificate (`/certificate/<student_id>/<workshop_id>/`).
- **Analytics Data Endpoint**: JSON API (`/analytics-data/`) for enrollments, attendance, and certificates.
- **Analytics Dashboard**: `/analytics/` page to visualize workshop stats.
- **Admin Interface**: Manage certificates with read-only issued date.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Django 5.2.6**
- **SQLite (default)** → Use PostgreSQL/MySQL for production
- **ReportLab** (for PDF certificate generation)

---

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd eventmanagement
   Create a Virtual Environment
   ```

bash
Copy code
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy code
pip install django reportlab
Apply Migrations

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a Superuser

bash
Copy code
python manage.py createsuperuser
Run the Development Server

bash
Copy code
python manage.py runserver
Access the Application

Admin: http://localhost:8000/admin/

Workshops: http://localhost:8000/workshops/

Analytics: http://localhost:8000/analytics/

ℹ️ Enrollment and Attendance are handled exclusively through the Django Admin Panel.
