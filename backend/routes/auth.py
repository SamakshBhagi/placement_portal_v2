from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from extensions import db
from schema import Company, Student, User
from datetime import timedelta, timezone, datetime
from utils.json_reply import respond

auth_bp = Blueprint("auth",__name__, url_prefix = "/api/auth")


@auth_bp.route("/register/student", methods = ["POST","OPTIONS"])
def register_student():
    if request.method == "OPTIONS":
        return "",200
    data = request.get_json(silent = True) or {}
    email = data.get("email").lower().strip()
    password = data.get("password")
    full_name = data.get("full_name").lower().strip()
    cgpa = data.get("cgpa")

    if not email or not password or not full_name:
        return respond(message="all fields needed", success=False, status=400)
    if User.query.filter_by(email = email).first():
        return respond(message="email already exists", success=False, status=400)
    hashed_password = generate_password_hash(password)
    new_user = User(email = email, pass_hash = hashed_password, role = "student")
    db.session.add(new_user)
    db.session.flush()

    new_student = Student(user_id = new_user.id, full_name = full_name, cgpa = cgpa)
    db.session.add(new_student)
    db.session.commit()

    return respond(
        data = {"student_id": new_student.student_id, "full_name": full_name, "email": email},
        message="Student has been registered",
        success = True, 
        status= 201
    )


@auth_bp.route("/register/company", methods = ["POST", "OPTIONS"])
def register_company():
    data = request.get_json(force = True)
    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")
    print(data)
    if not email or not password or not company_name: 
        return respond(message="all fields needed", success=False, status=400)
    if User.query.filter_by(email = email).first():
        return respond(message="email already exists", success=False, status=400)
    

    hashed_password = generate_password_hash(password)
    new_user = User(email = email, pass_hash = hashed_password, role = "company")
    db.session.add(new_user)
    db.session.flush()

    new_company = Company(user_id = new_user.id, company_name = company_name)
    db.session.add(new_company)
    db.session.commit()

    return respond(
        data = {"company_id": new_company.company_id, "company_name": company_name, "email": email},
        message="Company has been registered",
        success = True, 
        status= 201
    )

@auth_bp.route("/login", methods = ["POST", "OPTIONS"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email = email).first()
    if not user or not check_password_hash(user.pass_hash, password):
        return respond(message="invalid credentials", status = 401, success=False)
    
    if user.role == "company":
        company = Company.query.filter_by(user_id = user.id).first()
        if company.approval!="approved":
            return respond(message="Company not approved", status = 403, success=False)
        elif company.is_blacklisted:
            return respond(message="Company is blacklisted", status = 403, success=False)
    elif user.role=="student":
        student = Student.query.filter_by(user_id = user.id).first()
        if student.approval!="approved":
            return respond(message="Student not approved", status = 403, success=False)
        elif student.is_blacklisted:
            return respond(message="Student is blacklisted", status = 403, success=False)
    
    #real deal
    payload = {
        "user_id": user.id,
        "role": user.role, 
        "exp": datetime.now(timezone.utc) + timedelta(hours = 1)
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm = "HS256" )


    return respond(message="Logged in as " + user.role, success=True, data={"token":token,"user":{"id":user.id,
                                                                                                  "email":user.email,
                                                                                                  "role":user.role}})




