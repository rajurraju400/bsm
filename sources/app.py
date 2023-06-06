from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_migrate import Migrate

app = Flask(__name__, static_folder='Templates')
app.secret_key = 'your_secret_key'

# Configuring the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_sleep_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating the Database Instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
    

class SleepEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"SleepEntry(id={self.id}, date={self.date}, start_time={self.start_time}, end_time={self.end_time}, notes={self.notes})"
    
#Page to render the registration form


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate form inputs
        errors = {}

        # Check if username is provided and meets certain criteria
        if not username:
            errors['username'] = 'Username is required.'
        elif len(username) < 4:
            errors['username'] = 'Username must be at least 4 characters long.'

        # Check if email is provided and is a valid email address
        if not email:
            errors['email'] = 'Email is required.'
        elif not validate_email(email):
            errors['email'] = 'Invalid email address.'

        # Check if password is provided and meets certain criteria
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'

        # Check if confirm password matches the password
        if not confirm_password:
            errors['confirm_password'] = 'Confirm Password is required.'
        elif password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'

        if errors:
            # Render the registration form template with errors
            return render_template('register.html', errors=errors)

        # Create a new User instance
        new_user = User(username=username, email=email, password=generate_password_hash(password))

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful registration
        flash('Registration successful. Please continue to log in!!')
        return redirect(url_for('home'))

    # Render the registration form template
    return render_template('register.html')

#Page to render the login form from the registration form

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the user from the database based on the provided username
        user = User.query.filter_by(username=username).first()
        
        #Check if user exists 
        if user:

        # Verify the password
            if user and check_password_hash(user.password, password):
            # Create a session or token to authenticate the user
                session['user_id'] = user.id

            # Redirect to the home page after successful login
                return redirect(url_for('home'))
        else :
            return redirect(url_for('register'))

        # Handle invalid login credentials
        flash('Invalid username or password.')

    # Render the login form template
    return render_template('login.html')

#To render the home page
@app.route('/home')
def home():
    return render_template('home.html')

#To render the page to enter the sleep data 

@app.route('/sleep_entry', methods=['GET', 'POST'])
def sleep_entry():
    if request.method == 'POST':
        # Retrieve the form data
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        start_time = datetime.datetime.strptime(request.form['start_time'], '%H:%M').time()
        end_time = datetime.datetime.strptime(request.form['end_time'], '%H:%M').time()
        notes = request.form['notes']

        # Perform server-side validation
        errors = {}
        if date > datetime.date.today():
            errors['date'] = 'Date cannot be in the future.'
        if start_time >= end_time:
            errors['start_time'] = 'Start time must be before end time.'
        if len(notes) > 100:
            errors['notes'] = 'Notes should not exceed 100 characters.'

        if errors:
            # Render the sleep entry form template with errors
            return render_template('sleep_entry.html', errors=errors)

        # Create a new SleepEntry instance
        sleep_entry = SleepEntry(date=date, start_time=start_time, end_time=end_time, notes=notes)

        # Add the sleep entry to the database
        db.session.add(sleep_entry)
        db.session.commit()

        # Redirect to the sleep history page after submitting the form
        return redirect(url_for('sleep_history'))

    # Render the sleep entry form template
    return render_template('sleep_entry.html')

#Page to render the sleep history 

@app.route('/sleep_history')
def sleep_history():
    # Retrieve sleep entries from the database
    sleep_entries = SleepEntry.query.all()

    # Convert sleep entries to a JSON-serializable format
    sleep_entries_dict = []
    for entry in sleep_entries:
        entry_dict = {
            'id': entry.id,
            'date': entry.date.strftime('%Y-%m-%d'),
            'start_time': entry.start_time.strftime('%H:%M'),
            'end_time': entry.end_time.strftime('%H:%M'),
            'notes': entry.notes
        }
        sleep_entries_dict.append(entry_dict)

    # Render the sleep history template with the serialized sleep entries
    return render_template('sleep_history.html', sleep_entries=json.dumps(sleep_entries_dict))

#Validate email buil in function to validate the email entered 


def validate_email(email):
    # Email regular expression pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False




if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
