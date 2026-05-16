from celery import Celery
from app import create
import os
redis_url = os.getenv("REDIS_URL") 
def make_celery():
    app = create()
    celery = Celery(app.import_name, broker = redis_url, backend =redis_url )
    celery.conf.update(app.config)
    from celery.schedules import crontab

    celery.conf.beat_schedule = {

        "daily_reminder":{
            "task":"tasks.reminder_mail.daily_reminder",
            "schedule":crontab(hour = 9 , minute ="0")
        },

        "monthly_report":{
            "task":"tasks.monthly_report.monthly_report",
            "schedule":crontab( day_of_month = 1, hour = 9, minute = 0)
        }
    }
    taskbase = celery.Task
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return taskbase.__call__(self, *args, **kwargs)
    
    celery.Task = ContextTask
    return celery
celery = make_celery()
import tasks.test
import tasks.export_applications
import tasks.reminder_mail
import tasks.monthly_report
import tasks.selection_email