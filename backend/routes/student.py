from flask import request, g, Blueprint
from extensions import db
from utils.decorators import jwt_required
from utils.json_reply import respond
from schema import Company, Student, Drive, Application
from datetime import datetime

std_bp = Blueprint("student", __name__, url_prefix = "/api/student")

@std_bp.route("/dashboard")
@jwt_required("student")
def dashboard():
    user = g.current_user
    student = Student.query.filter_by(user_id = user.id).first()
    data = {
        "student_id": student.student_id,
        "name":student.full_name,
        "cgpa":student.cgpa,
        "resume_path":student.resume_path
    }
    return respond(message="fetched student data",data = data, success= True)



@std_bp.route("/drives", methods = ["GET"])
@jwt_required("student")
def get_valid_drives():
    user = g.current_user
    student = Student.query.filter_by(user_id = user.id).first() 
    page = request.args.get("page", 1, type = int)
    per_page = min(request.args.get("per_page",10, type = int), 50)
    search = request.args.get("search")

    query = Drive.query.filter(Drive.approval == "approved", Drive.deadline>datetime.utcnow(), Drive.cgpa_criteria<=student.cgpa).order_by(Drive.deadline.asc())

    if search:
        query = query.filter(Drive.role.ilike(f"%{search}%"))

    pagination = query.paginate(page = page, per_page = per_page, error_out = False)
    drives = pagination.items
    data = [{
        "drive_id": d.drive_id,
        "job_role": d.job_role,
        "ctc": d.ctc, 
        "deadline": d.deadline,
        "company":d.company.company_name 
    } for d in drives]

    return respond(message="drives for you", data = data, success = True, 
                   meta = {
                       "total_items":pagination.total,
                       "total_pages": pagination.pages, 
                       "page":page,
                       "per_page":per_page,
                       "has_next":pagination.has_next,
                       "has_prev":pagination.has_prev
                   })


@std_bp.route("/drives/<int:drive_id>/apply", methods = ["POST"])
@jwt_required("student")
def apply_drive(drive_id):
    std = g.current_user
    # convert to clean student usr.
    student = Student.query.filter_by(user_id = std.id).first()

    if not student:
        return respond(message= "Student not found!", success=False), 404
    if student.approval!="approved" or student.is_blacklisted:
        return respond(message = "Student is not eligible to apply", success = False), 403
    
    drive = Drive.query.get_or_404(drive_id)

    if drive.approval != "approved" or drive.status !="open":
        return respond(message="Drive not valid", success = False), 400
    
    if drive.deadline and drive.deadline< datetime.utcnow():
        return respond(message="deadline is over", success = False), 400
    
    if student.cgpa < drive.cgpa_criteria:
        return respond(message="Student cannot sit for this drive", success = False), 400
    
    duplicate = Application.query.filter_by(student_id = student.student_id, drive_id = drive.drive_id).first()
    if(duplicate):
        return respond(message = "Already applied to this drive!!", success = False), 400
    
    appn = Application(student_id = student.student_id, drive_id = drive.drive_id)
    db.session.add(appn)
    db.session.commit()
    return respond(message="Application given successfully", success = True, data = {
        "drive_id":drive_id,"student_id": student.student_id, "status":"applied"
    })

@std_bp.route("/view_applications", methods = ["GET"])
@jwt_required("student")
def view_applications():
    std = g.current_user
    student = Student.query.filter_by(user_id = std.id).first()

    # paginate, filter applications acc to student's id
    page = request.args.get("page",1, type = int)
    per_page = min(request.args.get("per_page", 10, type = int), 50 )
    query = Application.query.filter_by(student_id = student.student_id).order_by(Application.app_id.desc())

    pagination = query.paginate(page = page, per_page = per_page, error_out = False)
    applications = pagination.items
    data = [{
        "application_id": appn.app_id, 
        "drive_id": appn.drive_id, 
        "role":appn.drive.job_role,
        "company_name": appn.drive.company.company_name, 
        "status": appn.status,
        "applied_at": appn.applied_at
    } for appn in applications]

    return respond(message ="your drives", success = True, data = data, meta = {
        "total_items":pagination.total, 
        "total_pages":pagination.pages, 
        "page":page,
        "has_next":pagination.has_next, 
        "has_prev": pagination.has_prev,
        "per_page": per_page
    })

# async export jobs
@std_bp.route("/export_appn", methods = ["POST"])
@jwt_required("student")
def start_export_applications():
        
    from tasks.export_applications import export_applications
    from celery_app import celery
    from celery.result import AsyncResult

    std = g.current_user
    print(type(std), std)
    student = Student.query.filter_by(user_id = std.id).first()
    task = export_applications.delay(student.student_id )

    return respond(message="started the exports", success = True, data = {"task_id": task.id})


@std_bp.route("/export_appn_status/<task_id>", methods = ["GET"])
@jwt_required("student")
def application_export_status(task_id):
        
    from tasks.export_applications import export_applications
    from celery_app import celery
    from celery.result import AsyncResult

    task = AsyncResult(task_id, app = celery)
    if task.status == "PENDING":
        return respond(message="porcessing..", success=True)

    elif task.state == "SUCCESS":
        return respond(message="done!", success=True, data = task.result)
    elif task.status == "FAILURE":
        return respond(message = "Failed :((", success=False)
    return respond(message="working on it...", success=True)
 
from flask import send_from_directory

@std_bp.route("/download_file/<filename>", methods = ["GET"])
def download(filename):
    return send_from_directory("exports", filename, as_attachment = True)


import os
@std_bp.route("/upload-resume", methods = ["POST"])
@jwt_required("student")
def upload_resu():
    file = request.files.get("resume")
    
    student = Student.query.filter_by(user_id = g.current_user.id).first()
    name = f"student_{student.student_id}.pdf"
    path = os.path.join(f"uploads/resumes/{name}")
    file.save(path)
    student.resume_path = path
    db.session.commit()

    return respond(success=True)


from flask import send_file
@std_bp.route("/resume/<int:id>", methods = ["GET"])
@jwt_required("student")
def get_resu(id):
    student = Student.query.get(id)
    return send_file(student.resume_path,mimetype= "application/pdf")

@std_bp.route("/update", methods = ["PUT"])
@jwt_required("student")
def update():
    data = request.get_json()
    field = data.get("field")
    value = data.get("value")
    student = Student.query.filter_by(user_id = g.current_user.id).first()
    if field=="name":
        student.full_name = value
    else:
        student.cgpa = float(value)
    db.session.commit()
    
    return respond(success=True)