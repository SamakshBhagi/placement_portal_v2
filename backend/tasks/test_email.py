import smtplib
from email.mime.text import MIMEText

EMAIL_USER = "samaksh.bhagi.dev@gmail.com"
EMAIL_PASSWORD = "xowumjoywlvqmhtz"

msg = MIMEText("This is a test email from Placement App.")
msg["Subject"] = "SMTP Test Successful"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_USER, EMAIL_PASSWORD)
server.send_message(msg)
server.quit()

print("Email sent successfully")