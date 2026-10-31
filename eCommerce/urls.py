"""URL routing configuration for eCommerce storefront and vendor tools."""

from django.urls import path
from . import views

app_name = "eCommerce"

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("product/<int:product_id>/", views.product_page, name="product_page"),
    path(
        "product/<int:product_id>/review/",
        views.add_review,
        name="add_review",
    ),
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
    path("dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
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
    
    # M06T07 Task 1 API Endpoints
    path("api/stores/", views.api_stores_list, name="api_stores_list"),
    path("api/vendors/<int:vendor_id>/stores/", views.api_vendor_stores, name="api_vendor_stores"),
    path("api/stores/<int:store_id>/products/", views.api_store_products, name="api_store_products"),
    path("api/stores/<int:store_id>/reviews/", views.api_store_reviews, name="api_store_reviews"),
    
    path("reddit/", views.reddit_feed, name="reddit_feed"),
]
