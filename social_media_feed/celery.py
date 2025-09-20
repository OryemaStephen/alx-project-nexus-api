import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_feed.settings")

app = Celery("social_media_feed")

# Broker & backend should point to the Redis container service
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

# Optional settings
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'

# Autodiscover tasks
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
