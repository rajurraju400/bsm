from flask import Flask, render_template, request, redirect, url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuring the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_sleep_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating the Database Instance
db = SQLAlchemy(app)


class SleepEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"SleepEntry(id={self.id}, date={self.date}, start_time={self.start_time}, end_time={self.end_time}, notes={self.notes})"


@app.route('/')
def home():
    return render_template('home.html')


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
