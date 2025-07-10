from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import init_mysql
from MySQLdb.cursors import DictCursor

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Enable DictCursor for better access to column names
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = init_mysql(app)

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
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, password, role))
        mysql.connection.commit()
        flash("Registered successfully!")
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()

    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        flash("Login successful!")

        if user['role'] == 'hr':
            return redirect('/dashboard/hr')
        else:
            return redirect('/dashboard/employee')
    else:
        flash("Invalid credentials.")
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
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    jobs = cur.fetchall()
    return render_template('dashboard_employee.html', jobs=jobs)

# Optional: Temporary manual routes (can delete later)
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

    # Create users table
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

    # Create jobs table
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

if __name__ == '__main__':
    with app.app_context():
        initialize_database()

    app.run(debug=True)
