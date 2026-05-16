from flask import request, g, Blueprint
from extensions import db
from utils.decorators import jwt_required
from utils.json_reply import respond
from schema import Company, Student, Drive, Application
from datetime import datetime

company_bp = Blueprint("company",__name__, url_prefix = "/api/company")

@company_bp.route("/dashboard", methods = ["GET"])
@jwt_required("company")
def company_dash():
    # return company name, drive-wise applicants 
    user = g.current_user
    company = Company.query.filter_by(user_id = user.id).first()
    if not company:
        return respond(success=False, message="Invalid company")
    drives = Drive.query.filter_by(company_id = company.company_id).all()
    company_name = company.company_name
    data = [{
        "company_name":company_name,
        "drive_id":drive.drive_id,
        "role":drive.job_role,
        "applications":len(drive.applications),
        "approval":drive.approval,
        "deadline":drive.deadline.isoformat()
    } for drive in drives]
    return respond(message = "company data", success = True, data = data)



@company_bp.route("/drives", methods = ["POST"])
@jwt_required("company")
def create_drive():
    user= g.current_user
    company = Company.query.filter_by(user_id = user.id).first()
    if company.approval!="approved":
        return respond(message="not approved yet"), 403
    elif company.is_blacklisted:
        return respond(message="you have been blacklisted"), 403
    
    data = request.get_json()

    role = data.get("job_role")
    desc = data.get("job_desc")
    ctc = data.get("ctc")
    min_cgpa = data.get("cgpa_criteria")
    deadline = data.get("deadline")
    if not all([role, desc, ctc, min_cgpa, deadline]):
        return respond(message="kindly give all required fields"), 400
    
    try:
        deadline = datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        return respond(message="enter valid date")

    if deadline<=datetime.utcnow():
        return respond(message = "deadline must be a future date"), 400
    
    drive = Drive(company_id = company.company_id, job_role = role, job_desc = desc, ctc = ctc, deadline = deadline, cgpa_criteria = min_cgpa, approval = "pending")
    db.session.add(drive)
    db.session.commit()

    return respond(success = True, message= " drive created successfully..", data = {
        "drive_id": drive.drive_id, "job_role": drive.job_role, "deadline":drive.deadline.isoformat()
    })



@company_bp.route("/drives/<int:drive_id>/applications")
@jwt_required("company")
def drive_applicants(drive_id):
    user= g.current_user
    company = Company.query.filter_by(user_id  = user.id).first()
    if not company or company.approval !="approved":
        return respond(message="Company not approved", success = False)
    drive = Drive.query.filter_by(drive_id = drive_id, company_id = company.company_id).first_or_404()
    appn = Application.query.filter_by(drive_id = drive.drive_id)

    page = request.args.get("page",1,type = int)
    per_page = min(request.args.get("per_page", 10, type = int), 50)
    pagination = appn.paginate(page = page, per_page = per_page, error_out = False)
    applications = pagination.items

    data = [{
        "application_id":app.app_id,
        "student_id": app.student.student_id, 
        "student_name": app.student.full_name,
        "branch": app.student.branch,
        "status": app.status,
        "applied_at": app.applied_at.isoformat()

    } for app in applications]

    return respond(message = "Drive data", success = True, data = data, meta = {
        "total_items": pagination.total, 
        "total_pages": pagination.pages,
        "has_next": pagination.has_next, 
        "has_prev": pagination.has_prev,
        "page": page, 
        "per_page": per_page 
    })

@company_bp.route("/applications/<int:application_id>/status", methods = ["PUT"])
@jwt_required("company")
def update_application(application_id):
    user = g.current_user
    company = Company.query.filter_by(user_id = user.id).first()
    application = Application.query.get_or_404(application_id)

    if application.drive.company_id != company.company_id:
        return respond(message="Unauthorizd!", success = False)

    changed_status = request.json.get("status")

    application.status= changed_status
    if changed_status == "selected":
        from tasks.selection_email import selection_email
        selection_email.delay(application_id)
    db.session.commit()
    return respond(message="Changes the status", success = True, data = {
        "application_id":application.app_id, 
        "status":application.status
    }) 


@company_bp.route("/student/<int:id>",methods=["GET"])
@jwt_required("company")
def get_stud(id):
    student = Student.query.get_or_404(id)
    data= {
        "student_id":student.student_id,
        "name":student.full_name,
        "cgpa":student.cgpa,
        "resume_url":f"/api/company/student/{student.student_id}/resume"
    }
    return respond(data=data, success=True)

from flask import send_file
@company_bp.route("/student/<int:id>/resume",methods=["GET"])
@jwt_required("company")
def get_resume(id):
    student = Student.query.get_or_404(id)
    return send_file(student.resume_path, mimetype ="application/pdf")


# resumes ranked for the job description provided
# should show up on drive applicants page
# flow: for all applicants - > evaluate score- > return sorted list
# should i keep this as an async task?