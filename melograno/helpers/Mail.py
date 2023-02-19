from decouple import config
from django.core.mail import send_mail

class Mail:
    def __init__(self, subject, message, to_mail) -> None:
        self.subject = subject
        self.message = message
        self.to_mail = [ to_mail ]
        self.from_email = config('EMAIL_HOST_USER')

    def send(self):
        send_mail(
            self.subject,
            self.message,
            self.from_email,
            self.to_mail
        )