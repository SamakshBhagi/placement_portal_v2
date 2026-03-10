from celery_app import celery
@celery.task
def test():
    print("Working")
    return "Success"