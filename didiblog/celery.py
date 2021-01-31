from celery import Celery
from django.conf import settings
import os

# os.environ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'didiblog.settings')
app = Celery("test_celery")
app.conf.update(
    BROKER_URL='redis://@127.0.0.1:6379/1'
)
# 设置app自动发现任务
app.autodiscover_tasks(settings.INSTALLED_APPS)
