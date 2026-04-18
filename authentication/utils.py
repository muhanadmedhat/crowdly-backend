from django.core import signing
from django.core.mail import send_mail
from django.conf import settings
def generate_token(user):
    return signing.dumps(user.pk,salt="email-verification")

def verify_token(token):
    return signing.loads(token,salt="email-verification",max_age=900)

def send_verification_email(user):
    token = generate_token(user)
    verification_link = f"{settings.FRONTEND_URL}verify?token={token}"
    email_subject = "Verify your email"
    email_body = f"Please click the link below to verify your email:\n\n{verification_link}"
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER, 
        [user.email],
        fail_silently=False,
    )