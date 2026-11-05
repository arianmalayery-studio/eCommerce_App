"""Database models for storefronts, catalog items, orders, and customer
reviews.
"""

from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    """Digital storefront owned and managed by a vendor user."""

    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_manage_store", "Can manage vendor store"),
        ]

    def __str__(self):
        """Return the display name of the storefront."""
        return self.name


class Product(models.Model):
    """Catalog inventory item belonging to a store."""

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = [
            ("add_products", "Can add products"),
            ("change_products", "Can change products"),
            ("delete_products", "Can delete products"),
            ("view_products", "Can view products"),
        ]

    def __str__(self):
        """Return product name along with storefront affiliation."""
        store_name = self.store.name if self.store else "No Store"
        return f"{self.name} ({store_name})"


class Order(models.Model):
    """Customer purchase order record."""

    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        """Return unique order reference and buyer username."""
        return f"Order #{self.id} - {self.buyer.username}"


class OrderItem(models.Model):
    """Line item snapshot record within an order."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Return quantity, product name, and parent order reference."""
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"


class Review(models.Model):
    """Product feedback submitted by registered users."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return review summary with verification status."""
        status = "Verified" if self.is_verified else "Unverified"
        return f"{self.user.username} - {self.product.name} ({status})"
