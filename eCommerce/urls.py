"""URL Configuration for the eCommerce catalog, cart, and vendor portal."""

from django.urls import path
from . import views

app_name = "eCommerce"

urlpatterns = [
    # Catalog browsing
    path("", views.products_list, name="products_list"),
    path("all-products/", views.products_list, name="all_products"),
    path("stores/", views.stores_list, name="stores_list"),
    path(
        "stores/<int:store_id>/",
        views.store_products,
        name="store_products",
    ),
    path(
        "product/<int:product_id>/",
        views.product_page,
        name="product_page",
    ),
    path(
        "product/<int:product_id>/review/",
        views.add_review,
        name="add_review",
    ),
    # Shopping cart & checkout
    path("cart/", views.main_cart_page, name="main_cart_page"),
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "cart/update/<int:product_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    # Vendor dashboard & store management
    path(
        "vendor/dashboard/",
        views.vendor_dashboard,
        name="vendor_dashboard",
    ),
    path("vendor/reviews/", views.vendor_reviews, name="vendor_reviews"),
    path("store/create/", views.create_store, name="create_store"),
    path(
        "store/<int:store_id>/edit/",
        views.edit_store,
        name="edit_store",
    ),
    path(
        "store/<int:store_id>/delete/",
        views.delete_store,
        name="delete_store",
    ),
    # Vendor product management
    path(
        "store/<int:store_id>/product/add/",
        views.add_product,
        name="add_product",
    ),
    path(
        "product/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product",
    ),
    path(
        "product/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product",
    ),
    # Third-party integration
    path("reddit-feed/", views.reddit_feed, name="reddit_feed"),
]
