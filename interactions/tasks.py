from celery import shared_task

@shared_task
def add(x, y):
    """Simple task for CI testing"""
    return x + y
