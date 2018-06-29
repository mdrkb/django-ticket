from celery import shared_task
# from django_mailbox.management.commands.getmail import Command
from django.core import management


@shared_task
def fetch_tickets():
    management.call_command('getmail')
