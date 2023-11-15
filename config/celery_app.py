import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("news_feed_content")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# https://docs.celeryq.dev/en/main/userguide/periodic-tasks.html#available-fields
app.conf.beat_schedule = {
    "fetch-content-metadata-from-api": {
        "task": "config.tasks.fetch_content_metadata",
        "schedule": crontab(minute=25, hour=13),  # noqa
    },
}
