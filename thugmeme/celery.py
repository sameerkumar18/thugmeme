import os
import django
from celery import Celery
import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thugmeme.settings')
django.setup()


celery_app = Celery('tasks')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()  # [a for a in settings.INSTALLED_APPS])


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
