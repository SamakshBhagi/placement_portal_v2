from flask import Blueprint, request
from extensions import db
from utils.decorators import jwt_required
from utils.json_reply import respond
from schema import Company, Student, Drive, Application
from datetime import datetime
from utils.cache import get_cache, set_cache, delete_cache
from utils.cache import r
from flask import send_from_directory

admin_bp = Blueprint("admin",__name__, url_prefix ="/api/admin")

@admin_bp.route("/dashboard")
@jwt_required("admin")
def admin_dash():
    student_count = Student.query.count()
    company_count = Company.query.count()
    drive_count = Drive.query.filter(Drive.deadline<datetime.utcnow()).count() # gets all
    return respond(
        message="Curent stats",
        success= True, 
        data= {
            "student_count": student_count,
            "company_count": company_count,
            "drive_count": drive_count
        }
    )



# companies #

@admin_bp.route("/companies", methods = ["GET"])
#@admin_bp.route("/search/company")
@jwt_required(role ="admin")
def get_companies():
    search = request.args.get("search")
    page = request.args.get("page",1,type = int)
    per_page = request.args.get("per_page",10, type = int)
    cache_key = f"companies:{search}:{page}:{per_page}"
    cached = get_cache(cache_key)
    if cached:
        print("Cache Hit")
        return respond(**cached)
    print("Cache Missed")
    
    query = Company.query.order_by(Company.company_id.desc())
    
    if search:
        query = query.filter((Company.company_name.ilike(f"%{search}%")))

    pagination = query.paginate(page = page, per_page = per_page, error_out = False)
    companies = pagination.items 
    data = [{"id": c.company_id, "company_name":c.company_name, "is_blacklisted": c.is_blacklisted, "approval": c.approval} for c in companies]
    
    response ={
        "message":"List of companies",
        "data":data,
        "meta":{
            "page":page,
            "per_page": per_page, 
            "total_items": pagination.total,
            "total_pages": pagination.pages, 
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }
    set_cache(cache_key, response, ttl=15)
    return respond(**response)

@admin_bp.route("/companies/<int:company_id>/approve", methods = ["PUT"])
@jwt_required("admin")
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval = "approved"
    data = {"company_id":company.company_id, "company_name": company.company_name, "approval":company.approval}
    db.session.commit()
    delete_cache("companies:*")
    return respond(message="company approved", 
                data = data)


@admin_bp.route("/companies/<int:company_id>/reject", methods = ["PUT"])
@jwt_required("admin")
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval = "rejected"
    db.session.commit()
    delete_cache("companies:*")
    return respond(message="company rejected",
                data = {"company_id":company.company_id, "company_name": company.company_name, "approval":company.approval})


@admin_bp.route("/companies/<int:company_id>/blacklist", methods = ["POST"])
@jwt_required("admin")
def blacklist_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = True
    db.session.commit()
    delete_cache("companies:*")
    return respond(message="company blacklisted",
                 data = {"company_id":company.company_id, "company_name": company.company_name, "blacklist":company.is_blacklisted})

@admin_bp.route("/companies/<int:company_id>/unblacklist", methods = ["POST"])
@jwt_required("admin")
def unblacklist_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = False
    db.session.commit()

    delete_cache("companies:*")
    return respond(message="company unblacklisted", 
                   data = {"company_id":company.company_id, "company_name": company.company_name, "blacklist":company.is_blacklisted})



#students #
@admin_bp.route("/uploads/<path:filename>", methods = ["GET"])
#@jwt_required("admin")
def serve(filename):
    return send_from_directory("uploads", filename)

@admin_bp.route("/students")
#@admin_bp.route("/search/students")
@jwt_required("admin")
def get_students():
    search = request.args.get("search")
    query = Student.query.order_by(Student.student_id.desc())
    page = request.args.get("page", 1, type= int)
    per_page = request.args.get("per_page", 10, type = int)
    cache_key = f"students:{search}:{query}:{page}:{per_page}"
    cached = get_cache(cache_key)
    if cached:
        print("Cache hit")
        return respond(**cached)
    print("Cache miss")

    if search:
        query = query.filter(Student.full_name.ilike(f"%{search}%"))


    pagination = query.paginate(page = page, per_page = per_page, error_out = False)

    student = pagination.items



    data = [{"full_name": s.full_name, "is_blacklisted": s.is_blacklisted, "approval": s.approval, "cgpa":s.cgpa,"student_id":s.student_id,"resume_path":s.resume_path} for s in student]
    
    response = {"message":"Student list", "data" : data,  "meta" : {
        "page": page, 
        "per_page": per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev, 
        "total_items": pagination.total, 
        "total_pages": pagination.pages 
    }}
    set_cache(cache_key, response, ttl=15)
    return respond(**response)


@admin_bp.route("/students/<int:student_id>/approve", methods = ["PUT"])
@jwt_required("admin")
def approve_student(student_id):
    student= Student.query.get_or_404(student_id)
    student.approval = "approved"
    data = {"student_id":student.student_id, "full_name": student.full_name, "approval":student.approval}
    db.session.commit()
    delete_cache("students:*")
    return respond(message="student approved", 
                data = data)


@admin_bp.route("/students/<int:student_id>/reject", methods = ["PUT"])
@jwt_required("admin")
def reject_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.approval = "rejected"
    db.session.commit()
    delete_cache("students:*")
    return respond(message="student rejected",
                data = {"student_id":student.student_id, "full_name": student.full_name, "approval":student.approval})


@admin_bp.route("/students/<int:student_id>/blacklist", methods = ["POST"])
@jwt_required("admin")
def blacklist_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.is_blacklisted = True
    db.session.commit()
    delete_cache("students:*")
    return respond(message="student blacklisted",
                 data = {"student_id":student.student_id, "full_name": student.full_name, "blacklist":student.is_blacklisted})

@admin_bp.route("/students/<int:student_id>/unblacklist", methods = ["POST"])
@jwt_required("admin")
def unblacklist_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.is_blacklisted = False
    db.session.commit()


    delete_cache("students:*")
    return respond(message="student unblacklisted", 
                   data = {"student_id":student.student_id, "full_name": student.full_name, "blacklist":student.is_blacklisted})



# drives #
@admin_bp.route("/drives", methods = ["GET"])
@jwt_required("admin")   
def view_drives():
    search = request.args.get("search")
    approval= request.args.get("approval")
    page = request.args.get("page",1,type = int)
    per_page = min(request.args.get("per_page",10,type = int), 50)
    cache_key = f"drives:{search}:{approval}:{page}:{per_page}"
    cached = get_cache(cache_key)
    if cached:
        print("Cache Hit")
        return respond(**cached)
    print("Cache Miss")


    query = Drive.query.filter(Drive.deadline>datetime.utcnow()).order_by(Drive.drive_id.desc())

    if search:
        query = query.filter(Drive.job_role.ilike(f"%{search}%"))
    if approval:
        query= query.join(Company).filter(Drive.approval == approval, Drive.company.is_blacklisted==False)
    pagination = query.paginate(page = page, per_page=per_page, error_out = False)
    drives = pagination.items
    now = datetime.utcnow()
    data = [{
        "drive_id": d.drive_id, 
        "job_role": d.job_role,
        "ctc": d.ctc,
        "deadline": d.deadline.isoformat(),
        "approval": d.approval,
        "company":d.company.company_name,
        "app_count":len(d.applications),
        "status": "closed" if d.deadline < now else d.status
    } for d in drives]

    response = {"message":"all drives' data","data":data, "meta": {
        "page":page, "per_page": per_page, "total_items":pagination.total, "total_pages": pagination.pages,
        "has_next":pagination.has_next, "has_prev":pagination.has_prev}}
    set_cache(cache_key, response, ttl = 15)
    return respond(**response)


@admin_bp.route("/companies/<int:company_id>/drives", methods = ["GET"])
@jwt_required("admin")
def view_drives_by_company(company_id):
    comp = Company.query.get_or_404(company_id)
    if not comp:
        return respond(message= "company does not exist..", success= False)
    
    page = request.args.get("page", 1, type = int)
    per_page = min(request.args.get("per_page", 10, type = int), 50)
    query = Drive.query.filter(Drive.company_id==company_id, Drive.deadline>datetime.utcnow()).order_by(Drive.drive_id.desc())

    pagination = query.paginate(page = page, per_page = per_page, error_out = False)
    drives = pagination.items
    data = [{
        "drive_id": d.drive_id, 
        "job_role": d.job_role,
        "ctc":d.ctc,
        "approval":d.approval,
        "deadline":d.deadline.isoformat(),
     }for d in drives]
 
    return respond(
        message="drives of the company",
        success=True,
        data = data,
        meta = {"page":page, "per_page":per_page, "total_items":pagination.total, "total_pages":pagination.pages, "has_next":pagination.has_next,
                "has_prev":pagination.has_prev}
    )
    


@admin_bp.route("/drives/<int:drive_id>/approve", methods = ["PUT"])
@jwt_required("admin")
def approve_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.approval = "approved"
    db.session.commit()
    delete_cache("drives:*")
    return respond(message= " drive approved successfully..")


@admin_bp.route("/drives/<int:drive_id>/reject", methods = ["PUT"])
@jwt_required("admin")
def reject_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.approval = "rejected"
    db.session.commit()
    delete_cache("drives:*")
    return respond(message= " drive rejected..")



# view applications
@admin_bp.route("/applications", methods = ["GET"])
@jwt_required("admin")
def admin_appn_view():
    page = request.args.get("page",1,type = int)
    per_page = min(request.args.get("per_page",10, type = int ), 50)

    cache_key  = f"applications:{page}:{per_page}"
    cached = get_cache(cache_key)
    if cached:
        print("Cache hit")
        return respond(**cached)
    print("Cache miss")

    query = Application.query.order_by(Application.app_id.desc())
    pagination = query.paginate(page = page, per_page = per_page, error_out = False)

    applications = pagination.items

    data = [{
            "application_id": app.app_id, 
            "student_name": app.student.full_name,
            "company_name":app.drive.company.company_name,
            "job_role": app.drive.job_role,
            "status": app.status,
            "applied_at": app.applied_at.isoformat()

        } for app in applications]

    response = {"message": "Drive data",  "data" : data, "meta": {
            "total_items": pagination.total, 
            "total_pages": pagination.pages,
            "has_next": pagination.has_next, 
            "has_prev": pagination.has_prev,
            "page": page, 
            "per_page": per_page 
        }}
    set_cache(cache_key, response, ttl = 15)
    return respond(**response)
