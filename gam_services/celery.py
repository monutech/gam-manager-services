import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gam_services.settings')

app = Celery('proj', broker=os.environ.get('REDIS_URL'))

app.config_from_object('django.conf:settings', namespace='CELERY')
