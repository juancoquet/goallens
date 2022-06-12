from django.core.mail import send_mail # type: ignore
from django.shortcuts import render # type: ignore

from my_secrets import EMAIL_ADDRESS # type: ignore


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        msg = f'Name: {name}\nEmail: {contact}\n\n{message}'
        send_mail(subject, msg, '', [EMAIL_ADDRESS])
        message_sent = True
    else:
        message_sent = False
    return render(request, 'contact.html' , {'message_sent': message_sent})