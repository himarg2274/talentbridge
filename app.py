from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import init_mysql
from MySQLdb.cursors import DictCursor
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Enable DictCursor for better access to column names
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = init_mysql(app)

UPLOAD_FOLDER = 'static/resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('home'))

    if 'resume' not in request.files:
        flash("Resume file not found in request.")
        return redirect(url_for('employee_dashboard'))

    resume = request.files['resume']

    if resume.filename == '':
        flash("No file selected.")
        return redirect(url_for('employee_dashboard'))

    filename = secure_filename(f"{session['user_id']}_{int(time.time())}_{resume.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(filepath)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO applications (user_id, job_id, resume_path)
        VALUES (%s, %s, %s)
    """, (session['user_id'], job_id, filepath))
    mysql.connection.commit()

    flash("Applied successfully!")
    return redirect(url_for('employee_dashboard'))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Email already exists. Please use a different one.")
            return redirect(url_for('register'))

        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, password, role))
        mysql.connection.commit()
        flash("Registered successfully! You can now log in.")
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if user:
        if user['password'] == password:
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash("Login successful!")

            if user['role'] == 'hr':
                return redirect('/dashboard/hr')
            else:
                return redirect('/dashboard/employee')
        else:
            flash("Incorrect password.")
            return redirect('/')
    else:
        flash("Email not registered.")
        return redirect('/')

@app.route('/dashboard/hr', methods=['GET', 'POST'])
def hr_dashboard():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        department = request.form['department']
        location = request.form['location']
        skills = request.form['skills']

        cur.execute("""
            INSERT INTO jobs (title, description, department, location, skills_required)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, department, location, skills))
        mysql.connection.commit()

    cur.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    jobs = cur.fetchall()

    return render_template('dashboard_hr.html', jobs=jobs)

@app.route('/dashboard/employee')
def employee_dashboard():
    dept = request.args.get("department")
    location = request.args.get("location")
    skill = request.args.get("skill")

    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if dept:
        query += " AND department = %s"
        params.append(dept)
    if location:
        query += " AND location = %s"
        params.append(location)
    if skill:
        query += " AND skills_required LIKE %s"
        params.append(f"%{skill}%")

    query += " ORDER BY created_at DESC"

    cur = mysql.connection.cursor()

    # Get filtered jobs
    cur.execute(query, tuple(params))
    jobs = cur.fetchall()

    # Get unique departments and locations from DB
    cur.execute("SELECT DISTINCT department FROM jobs")
    departments = [row['department'] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT location FROM jobs")
    locations = [row['location'] for row in cur.fetchall()]

    cur.close()

    return render_template("dashboard_employee.html", jobs=jobs,
                           departments=departments, locations=locations)



@app.route('/employees/apply', methods=['GET', 'POST'])
def employee_apply():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        employee_id = request.form['employee_id']
        email = request.form['email']
        current_position = request.form['current_position']
        interested_position = request.form['interested_position']

        if 'resume' not in request.files:
            flash("No resume file found.")
            return redirect(url_for('employee_apply'))

        resume = request.files['resume']

        if resume.filename == '':
            flash("No file selected.")
            return redirect(url_for('employee_apply'))

        filename = secure_filename(f"{session['user_id']}_{int(time.time())}_{resume.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume.save(filepath)

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET name = %s, email = %s, skills = %s, resume_path = %s
            WHERE id = %s
        """, (name, email, f"Employee ID: {employee_id}, Current: {current_position}, Interested: {interested_position}", filepath, session['user_id']))
        mysql.connection.commit()

        flash("Application submitted successfully!")
        return redirect(url_for('employee_dashboard'))

    return render_template('employee_apply.html')

@app.route('/create-users-table')
def create_users_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            role ENUM('employee', 'hr'),
            skills TEXT,
            resume_path VARCHAR(255)
        )
    """)
    mysql.connection.commit()
    return "Users table created!"

@app.route('/create-jobs-table')
def create_jobs_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            department VARCHAR(100),
            location VARCHAR(100),
            skills_required TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    mysql.connection.commit()
    return "Jobs table created!"

def initialize_database():
    cur = mysql.connection.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            role ENUM('employee', 'hr'),
            skills TEXT,
            resume_path VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            department VARCHAR(100),
            location VARCHAR(100),
            skills_required TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    mysql.connection.commit()
    print("✅ Tables checked and initialized.")

@app.route('/create-applications-table')
def create_applications_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            job_id INT,
            status ENUM('Applied', 'Under Review', 'Interview Scheduled', 'Rejected', 'Selected') DEFAULT 'Applied',
            resume_path VARCHAR(255),
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)
    mysql.connection.commit()
    return "✅ Applications table created!"

if __name__ == '__main__':
    with app.app_context():
        initialize_database()
    app.run(debug=True)
