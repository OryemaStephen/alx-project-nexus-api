from django.core.management.base import BaseCommand
from interactions.tasks import add

class Command(BaseCommand):
    help = "Test Celery task in CI"

    def handle(self, *args, **kwargs):
        result = add.delay(3, 4)  # example task
        if result.get(timeout=10) == 7:
            self.stdout.write(self.style.SUCCESS("Celery task succeeded"))
        else:
            self.stdout.write(self.style.ERROR("Celery task failed"))
