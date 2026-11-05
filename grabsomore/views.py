"""Authentication, registration, and password recovery views for GrabSoMore."""

from datetime import timedelta
from hashlib import sha1
import secrets

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import ResetToken


def login_user(request):
    """Authenticate and log in registered users with session tracking."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.set_expiry(14 * 24 * 60 * 60)
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return HttpResponseRedirect(reverse("grabsomore:welcome"))
        return render(
            request,
            "grabsomore/login.html",
            {"error": "Invalid credentials."},
        )

    return render(request, "grabsomore/login.html")


def register_user(request):
    """Register users with password confirmation and unique email validation."""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        account_type = request.POST.get("account_type", "buyer")

        if password != password_confirm:
            return render(
                request,
                "grabsomore/register.html",
                {"error": "Passwords do not match."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "grabsomore/register.html",
                {"error": "That username is already taken."},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "grabsomore/register.html",
                {"error": "That email address is already registered."},
            )

        user = User.objects.create_user(
            username=username, password=password, email=email
        )

        if account_type == "vendor":
            vendor_group, _ = Group.objects.get_or_create(name="Vendors")
            user.groups.add(vendor_group)
        else:
            buyer_group, _ = Group.objects.get_or_create(name="Buyers")
            user.groups.add(buyer_group)

        try:
            permission = Permission.objects.get(
                codename="view_products",
                content_type__app_label="eCommerce",
            )
            user.user_permissions.add(permission)
        except Permission.DoesNotExist:
            pass

        user.save()
        login(request, user)
        return redirect("eCommerce:products_list")

    return render(request, "grabsomore/register.html")


def logout_user(request):
    """Log out user and redirect to login page."""
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("grabsomore:login"))


@login_required(login_url=reverse_lazy("grabsomore:login"))
def welcome(request):
    """Display protected welcome portal."""
    return render(request, "grabsomore/welcome.html")


def build_email(user, reset_url):
    """Construct password reset email message object."""
    subject = "Password Reset"
    domain_email = "noreply@grabsomore.local"
    body = (
        f"Hi {user.username},\n"
        f"Here is your link to reset your password: {reset_url}"
    )
    return EmailMessage(subject, body, domain_email, [user.email])


def generate_reset_url(user):
    """Generate secure, single-use token expiring in 5 minutes."""
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


def send_password_reset(request):
    """Dispatch password reset token to unique registered email."""
    if request.method == "POST":
        user_email = request.POST.get("email", "").strip()
        try:
            user = User.objects.get(email=user_email)
            reset_url = generate_reset_url(user)
            email = build_email(user, reset_url)
            email.send()
            return render(
                request,
                "grabsomore/reset_email_sent.html",
                {"email": user_email},
            )
        except (User.DoesNotExist, ObjectDoesNotExist):
            return render(
                request,
                "grabsomore/reset_email_sent.html",
                {"email": user_email},
            )

    return render(request, "grabsomore/request_password_reset.html")


def reset_user_password(request, token):
    """Validate incoming token from email link."""
    hashed_token = sha1(token.encode()).hexdigest()

    try:
        user_token = ResetToken.objects.get(token=hashed_token)

        if user_token.expiry_date < timezone.now():
            user_token.delete()
            return render(request, "grabsomore/password_reset_expired.html")

        request.session["user_id"] = user_token.user.id
        request.session["reset_token"] = token
        return render(
            request,
            "grabsomore/password_reset.html",
            {"token": token},
        )
    except ResetToken.DoesNotExist:
        return render(request, "grabsomore/password_reset_invalid.html")


def reset_password(request):
    """Update user password upon valid token verification."""
    if request.method == "POST":
        user_id = request.session.get("user_id")
        token = request.session.get("reset_token")
        password = request.POST.get("password")
        password_conf = request.POST.get("password_conf")

        if not all([user_id, token, password, password_conf]):
            return render(
                request,
                "grabsomore/password_reset.html",
                {
                    "error": "Missing fields or session expired.",
                    "token": token,
                },
            )

        if password != password_conf:
            return render(
                request,
                "grabsomore/password_reset.html",
                {"error": "Passwords do not match.", "token": token},
            )

        try:
            user = User.objects.get(id=user_id)
            hashed_token = sha1(token.encode()).hexdigest()
            reset_token = ResetToken.objects.get(token=hashed_token)

            if reset_token.expiry_date < timezone.now():
                reset_token.delete()
                return render(request, "grabsomore/password_reset_expired.html")

            user.set_password(password)
            user.save()
            reset_token.delete()
            request.session.flush()

            return HttpResponseRedirect(reverse("grabsomore:login"))
        except (User.DoesNotExist, ResetToken.DoesNotExist):
            return render(request, "grabsomore/password_reset_invalid.html")

    return HttpResponseRedirect(reverse("grabsomore:login"))
