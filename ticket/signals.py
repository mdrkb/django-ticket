from django_mailbox.signals import message_received
from django.dispatch import receiver


@receiver(message_received)
def fetch_mail(sender, message, **args):
    print('Message titled "%s" is received.' % (message.subject))
