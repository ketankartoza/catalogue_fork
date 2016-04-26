__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '4/27/16'

from celery.schedules import crontab

# daily every midnight
CELERYBEAT_SCHEDULE = {
    'exchange-update': {
        'task': 'tasks.exchange_update',
        'schedule': crontab(minute=0, hour=0),
    },
}

CELERY_TIMEZONE = 'UTC'