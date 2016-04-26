__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '4/27/16'


from django.core import management
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist


import logging
logger = logging.getLogger(__name__)

@shared_task(name='tasks.exchange_update')
def exchange_update():
    management.call_command('update_rates')