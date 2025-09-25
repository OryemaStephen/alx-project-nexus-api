# users/tasks.py
from celery import shared_task

@shared_task
def send_login_notification(user_email):

    print(f"Sending login notification to {user_email}")
    return f"Notification sent to {user_email}"
