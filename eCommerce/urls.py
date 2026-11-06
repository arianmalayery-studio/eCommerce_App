"""URL routing configuration for eCommerce storefront and vendor tools."""

from django.urls import path
from . import views

app_name = "eCommerce"

urlpatterns = [
    # Tiered Entry Points: Stores first, then store-specific products
    path("", views.stores_list, name="stores_list"),
    path("stores/", views.stores_list, name="stores"),
    path(
        "stores/<int:store_id>/products/", views.store_products, name="store_products"
    ),
    path("all-products/", views.products_list, name="products_list"),
    path("product/<int:product_id>/", views.product_page, name="product_page"),
    path(
        "product/<int:product_id>/review/",
        views.add_review,
        name="add_review",
    ),
    # Cart & Checkout
    path("cart/", views.main_cart_page, name="main_cart_page"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
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
    # Vendor Operations
    path("dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("vendor/reviews/", views.vendor_reviews, name="vendor_reviews"),
    path("store/new/", views.create_store, name="create_store"),
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
    path(
        "store/<int:store_id>/product/new/",
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
]
