# app.py
from flask import Flask, request, session, redirect, url_for, render_template, Response, send_file
from flaskext.mysql import MySQL
import pymysql
from flask_bootstrap import Bootstrap
from dataset_capture import dataset_capture_fun
from train import getImageswithId
from recognize import detect
from remove import removeFile,removeDir
from make_csv import writedata_to_csv,update_to_csv
from datetime import date
import csv
import re

app = Flask(__name__,static_folder="static11")

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'thisismysecretkey'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
bootstrap = Bootstrap(app)
mysql.init_app(app)

# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
             # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        id=request.form['id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE id = %s', (id))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'User id  already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user (id,username,password,email) VALUES (%s, %s, %s, %s)', (id,username, password, email))
            conn.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        id = session['id']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM course WHERE teacher_id = %s', (id))
        records = cursor.fetchall()
        print(list(records))
        conn.commit()

        return render_template('home.html', username=session['username'],courses=records)

    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))
    return redirect(url_for('login'))



# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM user WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/addCourse', methods=['GET', 'POST'])
def addCourse():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg=''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'course_id' in request.form and 'course_name' in request.form:
        # Create variables for easy access
        course_id=request.form['course_id']
        course_name = request.form['course_name']
        teacher_id=session['id']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM course WHERE course_id = %s', (course_id))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Course  already exists!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO course (course_id,course_name,teacher_id) VALUES (%s, %s, %s)', (course_id,course_name,teacher_id))
            msg = 'Course added Successfully!'

            cursor.execute('select student_id,student_name FROM student WHERE course_id = %s', (course_id))
            records = cursor.fetchall()
            conn.commit()
            writedata_to_csv(course_id, records)

    return render_template('addCourse.html',msg=msg)

@app.route('/addSudent', methods=['GET', 'POST'])
def addStudent():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg=''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'student_id' in request.form and 'student_name' in request.form and 'course_id' in request.form:
        # Create variables for easy access
        student_id=request.form['student_id']
        student_name = request.form['student_name']
        course_id = request.form['course_id']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM student WHERE student_id = %s', (student_id))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Student  already exists!'
        else:

            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO student (student_id,student_name,course_id) VALUES (%s, %s, %s)', (student_id,student_name,course_id))
            conn.commit()

            msg = 'Student added successfully!Now Please add student photo data.'

            session['student_id'] = student_id
            session['course_id'] = course_id

            record=[student_id,student_name]
            update_to_csv(course_id,record)

            return redirect(url_for('dataset_capture'))

    return render_template('addStudent.html',msg=msg)

@app.route('/dataset_capture',methods=['GET','POST'])
def dataset_capture():

   if request.method=='POST':
        student_id=session['student_id']
        course_id=session['course_id']

        dataset_capture_fun(student_id,course_id) #Data capuring

        path = 'dataSet/'  # setting out path of folders with images
        getImageswithId(path)     #Training data

        return redirect(url_for('addStudent'))
   return render_template('dataset_capture.html')

@app.route('/removeStudent',methods=['GET','POST'])
def removeStudent():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg=''

    if request.method == 'POST' and 'course_id' in request.form and 'student_id' in request.form:
        course_id = request.form['course_id']
        student_id = request.form['student_id']

        removeFile(student_id, course_id)  #Removing students photo data
        cursor.execute('DELETE FROM student WHERE student_id = %s', (student_id))
        conn.commit()
        msg='Student Removed'

    return render_template('removeStudent.html',msg=msg)

@app.route('/removeCourse', methods=['GET', 'POST'])
def removeCourse():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg=''
    if request.method == 'POST' and 'course_id' in request.form:
        course_id = request.form['course_id']

        removeDir(course_id)  # Removing students photo data
        cursor.execute('DELETE FROM student WHERE course_id = %s', (course_id))
        cursor.execute('DELETE FROM course WHERE course_id = %s', (course_id))
        conn.commit()
        msg='Course Removed'
    return render_template('removeCourse.html',msg=msg)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    records = []
    date_list = []

    if request.method == 'POST' and 'course_id' in request.form:
        course_id = request.form['course_id']
        detect(course_id)
        filename= course_id+'.csv'

        with open(filename,'r') as f:
            data = csv.reader(f)
            first_line = True
            today = date.today()
            today_str = str(today)
            date_list.append(today_str)

            for row in data:
                if not first_line:
                    records.append({
                        "student_id": row[0],
                        "student_name": row[1],
                        "date": row[2]
                    })
                else:
                    first_line = False

    return render_template('attendance.html',records=records,date_list=date_list)

#@app.route('/download_attendance/<course>', methods=['GET', 'POST'])
#def download_attendance(course):
#   print(course)
#    filename=course+'.csv'
#   return send_file(filename, mimetype="text/csv",attachment_filename="attendance.csv",as_attachment=True)

if __name__ == '__main__':
    app.run(debug="TRUE")