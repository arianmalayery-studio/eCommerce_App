"""URL Configuration for the grabsomore authentication app."""

from django.urls import path
from . import views

app_name = "grabsomore"

urlpatterns = [
    path("", views.login_user, name="login"),
    path("login/", views.login_user, name="login_alias"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("welcome/", views.welcome, name="welcome"),
    path(
        "request-password-reset/",
        views.send_password_reset,
        name="request_password_reset",
    ),
    path(
        "reset_password/<str:token>/",
        views.reset_user_password,
        name="reset_user_password",
    ),
    path(
        "password-reset-confirm/",
        views.reset_password,
        name="password_reset_confirm",
    ),
]
