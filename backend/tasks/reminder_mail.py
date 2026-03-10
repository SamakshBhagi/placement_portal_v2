import smtplib
from email.mime.text import MIMEText
from celery_app import celery
from datetime import datetime, timedelta
from schema import Drive, Student, User
from app import create

app = create()

def reminder_email(to, subject, body):
    from flask import current_app
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = current_app.config["EMAIL_USER"]
    msg["To"] = to
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(current_app.config["EMAIL_USER"], current_app.config["EMAIL_PASSWORD"])
    server.send_message(msg)
    server.quit()

@celery.task
def daily_reminder():
    with app.app_context():
        print("Sending reminders to students")

        upcoming = datetime.utcnow() + timedelta(days = 2)

        drives = Drive.query.filter(Drive.deadline>=datetime.utcnow(), Drive.deadline<=upcoming, Drive.approval=="approved").all()
        students = Student.query.filter_by(approval="approved").all()

        for d in drives:
            for s in students:
                user = User.query.get(s.user_id)
                reminder_email(to = user.email, subject ="Upcoming deadlines",
                         body = f'''Hi {s.full_name}!, The drive by {d.company.company_name}, for the role of {d.job_role} is closing, on {d.deadline}.
                         Please apply beforehand. Kindly ignore if already applied!
                        Regards
                        CDC, IITM''')

        return "Reminders sent!" 