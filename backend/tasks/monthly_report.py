from celery_app import celery
import smtplib
from datetime import datetime
from schema import Drive, Application
from email.mime.text import MIMEText

@celery.task
def monthly_report():
    
    now = datetime.utcnow()
    curr_day = datetime(now.year, now.month, 1)
    if now.month>1:
        last_day = datetime(now.year, now.month-1, 1)
    else:
        last_day = datetime(now.year -1 , now.month, 1)
    
    drives = Drive.query.all()
    drive_count = len(drives)

    applications = Application.query.all()
    appn_count = len(applications)

    selected = len([a for a in applications if a.status=="selected"])

    report = f'''
    <h2>Monthly Placement Report</h2>
    <ul>
        <li>Total drives: {drive_count}</li>
        <li>Total applications: {appn_count}</li>
        <li>Total students selected: {selected}</li>
    </ul>
    '''
    send_monthly_report(report)
    return "monthly report sent"

def send_monthly_report(html_content):
    from flask import current_app
    msg = MIMEText(html_content, "html")
    msg["Subject"] = "Monthly placement updates"
    msg["From"] = current_app.config["EMAIL_USER"]
    msg["To"] = current_app.config["EMAIL_USER"]
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(current_app.config["EMAIL_USER"], current_app.config["EMAIL_PASSWORD"])
    server.send_message(msg)
    server.quit()
        
        








