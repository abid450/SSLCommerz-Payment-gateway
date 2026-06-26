# Payment/__init__.py
from sl.celery import app as celery_app

__all__ = ('celery_app',)