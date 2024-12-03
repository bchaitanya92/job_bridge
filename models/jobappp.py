from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template

db = SQLAlchemy()
jobapp = Blueprint('jobapp', __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'employee' or 'employer'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employer = db.relationship('User', backref=db.backref('jobs', lazy=True))

    def __repr__(self):
        return f"Job('{self.title}', '{self.employer.username}')"

# Blueprint routes
@jobapp.route('/')
def home():
    return render_template('jobapp/index.html')

@jobapp.route('/employer/register', endpoint='employer_registration')
def employer_registration():
    return render_template('account/employer-registration.html')

@jobapp.route('/employee/register', endpoint='employee_registration')
def employee_registration():
    return render_template('account/employee-registration.html')

@jobapp.route('/job_list')
def job_list():
    return render_template('jobapp/job-list.html')

@jobapp.route('/job_detail/<int:job_id>')
def job_detail(job_id):
    return render_template('jobapp/job-detail.html', job_id=job_id)

@jobapp.route('/create_job')
@login_required
def create_job():
    return render_template('jobapp/create-job.html')
