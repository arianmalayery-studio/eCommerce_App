"""Serializers for the eCommerce REST API."""

from rest_framework import serializers
from .models import Store, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Product/Store Reviews."""

    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "user_username",
            "rating",
            "comment",
            "is_verified",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Store Products."""

    class Meta:
        model = Product
        fields = ["id", "store", "name", "description", "price", "stock"]
        read_only_fields = ["id", "store"]


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Stores."""

    vendor_username = serializers.ReadOnlyField(source="vendor.username")

    class Meta:
        model = Store
        fields = ["id", "vendor", "vendor_username", "name", "description"]
        read_only_fields = ["id", "vendor"]
