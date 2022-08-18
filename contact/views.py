from django.core.mail import send_mail # type: ignore
from django.shortcuts import render # type: ignore
from captcha.fields import ReCaptchaField # type: ignore
from captcha.widgets import ReCaptchaV2Checkbox # type: ignore
import requests
import os

from my_secrets import EMAIL_ADDRESS # type: ignore


def contact_view(request):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox).widget.render(
        'g-recaptcha-response', '', {})
    errors = []

    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        captcha_response = request.POST['g-recaptcha-response']
        verification_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': os.environ.get('RECAPTCHA_SECRET_KEY'),
                'response': captcha_response,
            }
        )
        if not verification_response.json()['success']:
            errors.append('Please verify that you are not a robot.')
            message_sent = False
        else:
            msg = f'Name: {name}\nEmail: {contact}\n\n{message}'
            send_mail(subject, msg, '', [EMAIL_ADDRESS])
            message_sent = True
    else:
        message_sent = False
    return render(request, 'contact.html' , {
        'message_sent': message_sent, 
        'captcha': captcha,
        'errors': errors,
        })