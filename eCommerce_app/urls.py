"""Root URL Configuration for eCommerce_app."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("grabsomore.urls")),
    path("ecommerce/", include("eCommerce.urls")),
    path("api/v1/", include("eCommerce.api_urls")),
]
