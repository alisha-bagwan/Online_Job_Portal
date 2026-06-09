
# 🧑‍💻 Online Job Portal

## 📌 Project Overview

The **Online Job Portal** is a web-based application developed using **Python Flask and MySQL**. It provides a platform for job seekers to register, log in, manage profiles, upload resumes, search for jobs, and apply for available positions.

The system also includes an **Admin Panel** for managing users and job postings.

This project was developed as a **Final Year BCA Project** to demonstrate skills in:
- Web Development
- Database Management
- User Authentication
- File Handling
- CRUD Operations

---

## 🚀 Features

### 👤 User Module
- User Registration
- User Login & Logout
- User Dashboard
- Profile Management
- Edit Profile
- Resume Upload & View
- Job Search
- View Available Jobs
- Apply for Jobs
- My Applications

---

### 🧑‍💼 Admin Module
- Admin Login Panel
- View All Users
- View All Jobs
- Delete Users
- Delete Jobs

---

### 🔐 Security Features
- Session-Based Authentication
- Protected Routes
- Login Validation
- Secure Access to Dashboard & Profile

---

## 🛠️ Technologies Used

### 🎨 Frontend
- HTML5
- CSS3
- Bootstrap 5
- Jinja2 Templates

### ⚙️ Backend
- Python
- Flask

### 🗄️ Database
- MySQL

### 🧰 Tools
- Visual Studio Code (VS Code)
- Git & GitHub
- MySQL Workbench

---

## 📂 Project Structure

```bash
Online-Job-Portal/
│
├── static/
│   ├── css/
│   └── resumes/
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── jobs.html
│   ├── add_job.html
│   ├── my_applications.html
│   ├── upload_resume.html
│   └── admin.html
│
├── app.py
└── README.md
```

---

## 🗄️ Database Structure

### 👤 users
- id (Primary Key)
- name
- email
- password
- resume

---

### 💼 jobs
- id (Primary Key)
- title
- company
- location
- salary
- description

---

### 📝 applications
- id (Primary Key)
- user_email
- job_id

---

## 🎯 Learning Outcomes

- Flask Web Development
- MySQL Integration
- CRUD Operations
- Authentication System
- Session Management
- File Upload Handling
- UI Design with Bootstrap
- Git & GitHub Version Control

---


## 🌟 Future Enhancements

- Email Notifications
- Password Encryption (Hashing)
- Profile Picture Upload
- Job Category System
- Advanced Job Filtering
- Application Status Tracking
- Deployment on Cloud (AWS / Render / Railway)

---

## 👩‍💻 Author

**Alisha Bagwan**  
Bachelor of Computer Applications (BCA)  
Final Year Project

---

## 📌 Note

This project is created for academic learning purposes and demonstrates full-stack web development using Flask and MySQL.




