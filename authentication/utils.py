from django.core import signing
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from accounts.models import UserProfile

def generate_token(user):
    return signing.dumps(user.pk,salt="email-verification")

def verify_token(token):
    return signing.loads(token,salt="email-verification",max_age=86400)

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
def send_reset_password(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"{settings.FRONTEND_URL}reset-password?uid={uid}&token={token}"
    email_subject = "Reset your password"
    email_body = f"Please click the link below to reset your password:\n\n{reset_link}"
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def reset_verify_token(uid, token):
    try:
        pk = force_str(urlsafe_base64_decode(uid))
        user = UserProfile.objects.get(pk=pk)
        if default_token_generator.check_token(user, token):
            return user
    except Exception:
        pass
    return None