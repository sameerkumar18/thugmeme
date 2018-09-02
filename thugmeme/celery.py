import os

import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thugmeme.settings')
django.setup()

celery_app = Celery('tasks')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# from thugmeme import settings
celery_app.autodiscover_tasks(force=True)  # [a for a in settings.INSTALLED_APPS])


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
