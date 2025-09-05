# 🌉 TalentBridge – Internal Job Portal

A Flask + MySQL web application for employees to explore internal job opportunities and for HR to manage job postings within an organization.

🔗 GitHub Repo: https://github.com/himarg2274/talentbridge.git

---

## 📌 Features

- User registration and login (Employee or HR)
- HR can post, view, and manage jobs
- Employees can browse internal jobs
- Uses MySQL for database (via MySQL Workbench/CLI)
- Tables are auto-created on first run
- Simple UI for beginners

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (created via MySQL Workbench or CLI)
- **Frontend:** HTML 
- **ORM:** Flask-MySQLdb

---

## 🚀 How to Run the Project (Step-by-Step)

### ✅ 1. Install Required Tools

- **Python** (3.10 or above): https://www.python.org/downloads/
- **Git**: https://git-scm.com/downloads
- **MySQL Server** (instal MySQL Workbench)

### ✅ 2. Clone the Repository

```bash
git clone https://github.com/himarg2274/talentbridge.git
cd talentbridge
```

### ✅ 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### ✅ 4. Install Required Python Packages

```bash
pip install Flask flask-mysqldb
```

### ✅ 5. Create the MySQL Database

🔐 Use your MySQL password when prompted (e.g., `Root12345`).

Open **MySQL Command Line Client** or **MySQL Workbench**, and run:

```sql
CREATE DATABASE talentbridge;
```

### ✅ 6. Update `db_config.py` with Your MySQL Credentials

Edit the `db_config.py` file and set your MySQL password:

```python
from flask_mysqldb import MySQL

def init_mysql(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Root12345'  # 👈 your password here
    app.config['MYSQL_DB'] = 'talentbridge'
    return MySQL(app)
```

### ✅ 7. Run the Flask App

```bash
python app.py
```

Go to your browser and open:

```
http://localhost:5000
```

---
````
talentbridge/
│
├── app.py                  # Main Flask app
├── db_config.py            # DB connection setup
├── templates/              # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard_hr.html
│   └── dashboard_employee.html
├── static/                 # Optional folder for CSS/JS
├── tests/                  # Robot Framework test cases
│   ├── login_tests.robot
│   ├── job_posting_tests.robot
│   └── application_flow_tests.robot
└── README.md               # This file
````
---

## ✅ What Happens When You Run the App?

- Connects to MySQL
- Automatically creates required tables:
  - `users`
  - `jobs`
- You can now:
  - Register as **HR** or **Employee**
  - Login and go to respective dashboards
  - **HR** can post and view job listings
  - **Employees** can view job listings  
  *(Apply feature and resume upload coming soon)*

---
## ✅ Covered Scenarios

### 🔐 Login Tests
- Valid Employee login  
- Valid HR login  
- Invalid login (wrong password / unknown user)  

### 💼 Job Posting & Application
- HR posts a new job  
- Employee searches jobs (by department, location, skills)  
- Employee applies for a job  

### 👤 Profile & Notifications
- Resume upload  
- Application status tracking  
- HR interview scheduling  
- Notifications for new jobs  

### 🔒 Security & Reliability
- Password reset  
- Multiple failed login attempts → account lock  
- Session timeout handling  

---

## 🚀 How to Run Tests

### 1️⃣ Install Robot Framework and Selenium

```bash
pip install robotframework
pip install robotframework-seleniumlibrary
```
### 2️⃣ Run the Test Suite
```bash
robot tests/
```
## 🛠️ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `Access denied for user 'root'@'localhost'` | Check password in `db_config.py` |
| `Unknown database 'talentbridge'` | Run `CREATE DATABASE talentbridge;` in MySQL |
| `Table 'users' or 'jobs' doesn't exist` | Just re-run `app.py` – tables are auto-created |

---




