from django.test import TestCase # type: ignore
from unittest.mock import patch


class TestContactView(TestCase):

    def test_uses_contact_template(self):
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response, 'contact.html')

    def test_response_contains_contact_form(self):
        response = self.client.get('/contact/')
        self.assertContains(response, 'id="contact-form"')

    def test_form_contains_fields(self):
        response = self.client.get('/contact/')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="subject"')
        self.assertContains(response, 'name="message"')

    def test_post_displays_success_message(self):
        response = self.client.post('/contact/', {
            'name': 'John Doe',
            'email': 'john@doe.com',
            'subject': 'Test subject',
            'message': 'Test message',
        })
        self.assertContains(response, 'Your message has been sent.')

    @patch('contact.views.send_mail')
    def test_send_mail_is_called(self, mock_send_mail):
        self.client.post('/contact/', {
            'name': 'John Doe',
            'email': 'john@doe.com',
            'subject': 'Test subject',
            'message': 'Test message',
        })
        self.assertTrue(mock_send_mail.called)
