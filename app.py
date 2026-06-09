from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
import os

UPLOAD_FOLDER = 'static/resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'jobportal'

# MYSQL CONFIGURATION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

# Enter your MySQL password
app.config['MYSQL_PASSWORD'] = 'alisha@20'

app.config['MYSQL_DB'] = 'jobportal'

mysql = MySQL(app)


# HOME PAGE
@app.route('/')
def home():
    return render_template("index.html")


# REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        mysql.connection.commit()

        cur.close()

        return redirect('/login')

    return render_template("register.html")

   # LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            session['email'] = email


            return redirect('/dashboard')

        else:

            return "Invalid Email or Password"

            return redirect('/login')

    return render_template("login.html")


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    # Total Jobs
    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    # Total Applications
    cur.execute("SELECT COUNT(*) FROM applications")
    total_applications = cur.fetchone()[0]

    # Total Users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.close()

    return render_template(
        "dashboard.html",
        total_jobs=total_jobs,
        total_applications=total_applications,
        total_users=total_users
    )


    # LOGOUT
@app.route('/logout')
def logout():

    # Remove session
    session.pop('email', None)

    return redirect('/login')


# ADD JOB
@app.route('/add-job', methods=['GET', 'POST'])
def add_job():

    if request.method == 'POST':

        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        salary = request.form['salary']
        description = request.form['description']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO jobs(title, company, location, salary,description)
            VALUES(%s,%s,%s,%s,%s)
            """,
            (title, company, location, salary, description)
        )

        mysql.connection.commit()

        cur.close()

        
        return redirect('/jobs')

    return render_template("add_job.html")



    

# APPLY JOB
@app.route('/apply/<int:job_id>')
def apply(job_id):

    if 'email' not in session:
        return redirect('/login')

    user_email = session['email']

    cur = mysql.connection.cursor()

    # Check if already applied
    cur.execute(
        """
        SELECT * FROM applications
        WHERE user_email=%s AND job_id=%s
        """,
        (user_email, job_id)
    )

    existing = cur.fetchone()

    if existing:

        cur.close()

        return "You have already applied for this job."

    # Insert application
    cur.execute(
        """
        INSERT INTO applications(user_email, job_id)
        VALUES(%s,%s)
        """,
        (user_email, job_id)
    )

    mysql.connection.commit()

    cur.close()

    return "Application Submitted Successfully!"

    # MY APPLICATIONS
@app.route('/my-applications')
def my_applications():

    # Check login
    if 'email' in session:

        user_email = session['email']

        cur = mysql.connection.cursor()

        # JOIN query
        cur.execute("""
            SELECT jobs.title,
                   jobs.company,
                   jobs.location,
                   jobs.salary
            FROM applications
            JOIN jobs
            ON applications.job_id = jobs.id
            WHERE applications.user_email = %s
        """, (user_email,))

        applications = cur.fetchall()

        cur.close()

        return render_template(
            "my_applications.html",
            applications=applications
        )

    else:
        return redirect('/login')



        # JOBS PAGE
@app.route('/jobs')
def jobs():

    search = request.args.get('search')

    cur = mysql.connection.cursor()

    if search:

        cur.execute(
            "SELECT * FROM jobs WHERE title LIKE %s",
            ('%' + search + '%',)
        )

    else:

        cur.execute("SELECT * FROM jobs")

    all_jobs = cur.fetchall()

    cur.close()

    return render_template(
        "jobs.html",
        jobs=all_jobs
    )

# PROFILE PAGE
@app.route('/profile')
def profile():

    if 'email' not in session:
        return redirect('/login')

    email = session['email']

    cur = mysql.connection.cursor()

    # Get user details including resume
    cur.execute(
        "SELECT name, email, resume FROM users WHERE email=%s",
        (email,)
    )

    user = cur.fetchone()

    cur.close()

    return render_template(
        "profile.html",
        user=user
    )
# JOB DETAILS
@app.route('/job/<int:id>')
def job_details(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (id,)
    )

    job = cur.fetchone()

    cur.close()

    return render_template(
        "job_details.html",
        job=job
    )


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():

    if 'email' not in session:
        return redirect('/login')

    email = session['email']

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']

        cur.execute(
            """
            UPDATE users
            SET name=%s, password=%s
            WHERE email=%s
            """,
            (name, password, email)
        )

        mysql.connection.commit()

        cur.close()

        return redirect('/profile')

    cur.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cur.fetchone()

    cur.close()

    return render_template(
        "edit_profile.html",
        user=user
    )


# DELETE JOB
@app.route('/delete-job/<int:id>')
def delete_job(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM jobs WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    return redirect('/jobs')


#upload resume

@app.route('/upload-resume', methods=['GET', 'POST'])
def upload_resume():

    if 'email' not in session:
        return redirect('/login')

    if request.method == 'POST':

        file = request.files['resume']

        if file:

            filename = file.filename

            file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

            cur = mysql.connection.cursor()

            cur.execute(
                """
                UPDATE users
                SET resume=%s
                WHERE email=%s
                """,
                (filename, session['email'])
            )

            mysql.connection.commit()

            cur.close()

            return redirect('/profile')

    return render_template('upload_resume.html')

#Admin Route
@app.route('/admin')
def admin():

    cur = mysql.connection.cursor()

    # Total Users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Total Jobs
    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    # Total Applications
    cur.execute("SELECT COUNT(*) FROM applications")
    total_applications = cur.fetchone()[0]

    # All Users
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    # All Jobs
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()

    cur.close()

    return render_template(
        "admin.html",
        users=users,
        jobs=jobs,
        total_users=total_users,
        total_jobs=total_jobs,
        total_applications=total_applications
    )

#Delete User Feature
@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect('/admin')
if __name__ == '__main__':
    app.run(debug=True)