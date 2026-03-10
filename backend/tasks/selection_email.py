import smtplib
from celery_app import celery
from schema import User, Application
from email.mime.text import MIMEText

@celery.task()
def selection_email(application_id):
    from flask import current_app
    appn = Application.query.get(application_id)

    student = appn.student
    drive = appn.drive
    company  = drive.company

    msg = MIMEText(f'''
    Hi {student.full_name}!
    Congratulations! You have been selected for the role of {drive.job_role}
    at {company.company_name}.
    For further steps, kindly contact the CDC in person.
    Regards,
    CDC IITM''')
    user = User.query.get(student.user_id)

    msg["Subject"] = "Congratulations!"
    msg["From"] = current_app.config["EMAIL_USER"]
    msg["To"] = user.email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(current_app.config["EMAIL_USER"], current_app.config["EMAIL_PASSWORD"])
    server.send_message(msg)
    server.quit()
    return "selection email sent"