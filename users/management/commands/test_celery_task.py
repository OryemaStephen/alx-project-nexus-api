from django.core.management.base import BaseCommand
from interactions.tasks import add  # your sample celery task

class Command(BaseCommand):
    help = "Test Celery task"

    def handle(self, *args, **kwargs):
        result= add.delay(5, 7)  # example task
        if result.get(timeout=10) == 12:
            self.stdout.write(self.style.SUCCESS("Celery task succeeded"))
        else:
            self.stdout.write(self.style.ERROR("Celery task failed"))
