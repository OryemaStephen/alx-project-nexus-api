import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_feed.settings")

app = Celery("social_media_feed")

# Use RabbitMQ as broker, Redis as result backend
app.conf.broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    "cleanup-old-posts-daily": {
        "task": "posts.tasks.cleanup_old_posts",
        "schedule": crontab(hour=0, minute=0),  # every day at midnight
        "args": (365,),  # posts older than 1 year
    },
    "log-post-metrics-hourly": {
        "task": "posts.tasks.log_post_metrics",
        "schedule": crontab(minute=0, hour="*"),  # every hour
    },
}