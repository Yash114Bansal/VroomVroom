import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vroomvroom.settings")

app = Celery("vroomvroom")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'process-chat-messages-every-5-seconds': {
        'task': 'chat.tasks.process_chat_messages',
        'schedule': 5.0,
    },
}
