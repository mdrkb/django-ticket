from django.shortcuts import render, get_object_or_404
from django_mailbox.models import Message


def ticket_list(request):
    tickets = Message.incoming_messages.filter(in_reply_to=None).order_by('-id')
    return render(request, 'ticket/ticket_list.html', {'tickets': tickets})


def ticket_details(request, ticket_id):
    ticket = get_object_or_404(Message, id=ticket_id)

    responses = []
    response = True

    if ticket:
        while response:
            try:
                response = Message.objects.get(in_reply_to=ticket_id)
                ticket_id = response.id
                responses.append(response)
            except Message.DoesNotExist:
                response = False

    return render(request, 'ticket/ticket_details.html', {'ticket': ticket, 'responses': responses})
