from datetime import timedelta
from hashlib import sha1
import secrets

from django.core.mail import EmailMessage
from django.utils import timezone

from .models import ResetToken


def build_email(user, reset_url):
    subject = "Password Reset"
    domain_email = "noreply@grabsomore.local"
    body = (
        f"Hi {user.username},\n"
        f"Here is your link to reset your password: {reset_url}"
    )
    return EmailMessage(subject, body, domain_email, [user.email])


def generate_reset_url(user):
    domain = "http://127.0.0.1:8000/"
    app_name = "grabsomore"
    url = f"{domain}{app_name}/reset_password/"

    token = secrets.token_urlsafe(16)
    expiry_date = timezone.now() + timedelta(minutes=5)
    hashed_token = sha1(token.encode()).hexdigest()

    ResetToken.objects.create(
        user=user,
        token=hashed_token,
        expiry_date=expiry_date,
    )

    return f"{url}{token}/"
