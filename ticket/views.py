from django.shortcuts import render, get_object_or_404
from django_mailbox.models import Message
from .forms import TicketResponseForm
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.contrib import messages
import logging
import bleach

logger = logging.getLogger(__name__)


def ticket_list(request):
    tickets = Message.incoming_messages.filter(in_reply_to=None).order_by('-id')
    return render(request, 'ticket/ticket_list.html', {'tickets': tickets})


def ticket_details(request, ticket_id):
    try:
        ticket = get_object_or_404(Message, id=ticket_id)

        responses = []
        response = True
        response_id = ticket_id

        while response:
            try:
                response = Message.objects.get(in_reply_to=response_id)
                response_id = response.id
                responses.append(response)

            except Message.DoesNotExist:
                response = False

        if request.method == 'POST':
            form = TicketResponseForm(request.POST)

            if form.is_valid():
                response_id = form.cleaned_data.get('response')
                message_plain = form.cleaned_data.get('message')
                message_html = message_plain.replace('\r', '<br />')

                try:
                    last_response = Message.objects.get(id=int(response_id))

                    email_message = EmailMultiAlternatives(
                        body=message_plain,
                        subject=last_response.subject,
                        to=[last_response.from_address],
                    )
                    email_message.attach_alternative(message_html, 'text/html')

                    last_response.reply(email_message)
                    messages.success(request, 'Response send successfully.', extra_tags='success')

                    form = TicketResponseForm({'response': response_id})

                except Exception as err:
                    messages.error(request, 'Failed to send response. Error: ' + str(err), extra_tags='danger')
        else:
            form = TicketResponseForm({'response': response_id})

        return render(request, 'ticket/ticket_details.html',
                      {'ticket': ticket, 'responses': responses, 'form': form})

    except Exception as err:
        logger.error('Error: ' + str(err))
