import os, csv
from celery_app import celery
from datetime import datetime
from schema import Company, User, Drive, Student, Application
from extensions import db
from utils.json_reply import respond

folder = "exports"
#export student  applications as csv
@celery.task
def export_applications(student_id):
    os.makedirs(folder, exist_ok=True)
    student= Student.query.filter_by(student_id = student_id).first()
    if not student:
        return respond(message="Student not found",success = False)
    applications = Application.query.filter_by(student_id=student_id).all()

    name = f"{student_id}_{datetime.utcnow().timestamp()}_appn.csv"
    path = os.path.join(folder, name)
    with open(path, mode="w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(["Id", "Company","Role","Status","Applied on"])
        
        
        for appn in applications:    
            writer.writerow([ student.student_id,
            appn.drive.company.company_name,
            appn.drive.job_role,
            appn.status, 
            appn.applied_at.isoformat() ])
        
    
    return {"status":"exported your applications", "file":name, "path":path}