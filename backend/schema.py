from datetime import datetime, timezone
from extensions import db
from flask_login import UserMixin
from sqlalchemy import Enum

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, index = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    pass_hash = db.Column(db.String(100), nullable = False)
    role = db.Column(Enum("student", "company", "admin", name = "user_role"), default = "student")
    is_active = db.Column(db.Boolean, default = True)
    created = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

class Student(db.Model):
    __tablename__ = "student"
    applications = db.relationship("Application", backref = "student", cascade= "all, delete-orphan")
    student_id= db.Column(db.Integer, primary_key = True, index = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable = False, index = True)
    full_name = db.Column(db.String(100), index = True)
    branch = db.Column(db.String(100))
    cgpa = db.Column(db.Float, index = True, nullable = False)
    grad_year = db.Column(db.Integer)
    resume_path = db.Column(db.String(200))
    approval = db.Column(Enum("pending", "approved", "rejected", name = "std_approval_status"), default = "pending", nullable = False)
    is_blacklisted = db.Column(db.Boolean, default = False)

class Company(db.Model):
    __tablename__="company"
    company_id = db.Column(db.Integer, primary_key = True, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False, index = True)
    company_name = db.Column(db.String(100), index = True)
    website = db.Column(db.String(100))
    approval = db.Column(Enum("pending", "approved", "rejected", name = "cmp_approval_status"), default = "pending", nullable = False)
    is_blacklisted = db.Column(db.Boolean, default = False)

class Drive(db.Model):
    __tablename__ = "drive"
    company = db.relationship("Company", backref = "drives")
    applications = db.relationship("Application", backref = "drive", cascade = "all, delete-orphan") 
    drive_id = db.Column(db.Integer, primary_key = True, index = True) # surrogate key, ideally should be a weak entity with total participation.
    company_id = db.Column(db.Integer, db.ForeignKey("company.company_id"), nullable = False, index = True)
    job_role = db.Column(db.String(100), nullable = False)
    job_desc = db.Column(db.Text) 
    cgpa_criteria = db.Column(db.Float, index = True)
    branch_criteria = db.Column(db.String(100)) 
    ctc = db.Column(db.Integer, nullable = False, index = True)
    deadline = db.Column(db.DateTime)
    status = db.Column(Enum("open","closed", name = "drive_status"), default = "open", nullable = False)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    approval = db.Column(Enum("pending", "approved", "rejected", name = "drive_approval_status"), default = "approved", nullable = False)

class Application(db.Model):
    __tablename__ = "application"
    app_id = db.Column(db.Integer, primary_key =True, index = True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable = False, index = True)
    drive_id = db.Column(db.Integer, db.ForeignKey("drive.drive_id"), nullable = False, index = True)
    score = db.Column(db.Integer)
    applied_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    status = db.Column(Enum("applied","shortlisted", "selected", "rejected", name = "application_status"), default = "applied", nullable = False)
    updated_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("student_id", "drive_id", name = "unique_appn"),)
