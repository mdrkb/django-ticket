from django.apps import AppConfig


class TicketConfig(AppConfig):
    name = 'ticket'

    def ready(self):
        import ticket.signals
