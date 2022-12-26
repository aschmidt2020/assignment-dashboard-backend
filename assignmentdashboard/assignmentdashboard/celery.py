import os
from datetime import date, timedelta
from celery import Celery
from celery.schedules import crontab
from django.apps import apps

# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
# celery -A assignmentdashboard worker -l INFO
# brew services start rabbitmq

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignmentdashboard.settings')

app = Celery('assignmentdashboard')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'UTC'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=1, minute=0),
#         mark_archived_assignments.s(),
#     )

@app.task
def mark_archived_assignments():
    archive_date = date.today() - timedelta(days = 3)
    assignment_model = apps.get_model('assignment', 'Assignment')
    assignments_to_be_archived = list(assignment_model.objects.filter(assignment_due_date__lte=(archive_date)))
    for assignment in assignments_to_be_archived:
        assignment.assignment_archived = True
        assignment.save()
