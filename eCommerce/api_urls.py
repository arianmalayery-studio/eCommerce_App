"""API v1 URL routing for eCommerce endpoints."""

from django.urls import path
from . import api_views

app_name = "ecommerce_api_v1"

urlpatterns = [
    path("stores/", api_views.api_stores_list, name="stores_list"),
    path(
        "vendors/<int:vendor_id>/stores/",
        api_views.api_vendor_stores,
        name="vendor_stores",
    ),
    path(
        "stores/<int:store_id>/products/",
        api_views.api_store_products,
        name="store_products",
    ),
    path(
        "stores/<int:store_id>/reviews/",
        api_views.api_store_reviews,
        name="store_reviews",
    ),
]
