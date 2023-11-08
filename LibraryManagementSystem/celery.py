# LibraryManagementSystem/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSystem.settings')

app = Celery('LibraryManagementSystem')

# Using a string here means the worker doesn't have to serialize the configuration object.
# This step ensures that the configuration is stored in the environment variables.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
