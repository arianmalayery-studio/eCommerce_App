"""REST API views for eCommerce storefronts, products, and reviews (v1)."""

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Review, Store
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    StoreSerializer,
)


def check_is_vendor(user):
    """Check if the user belongs to the Vendors group or is staff."""
    if not user or not user.is_authenticated:
        return False
    return user.is_staff or user.groups.filter(name="Vendors").exists()


@api_view(["GET", "POST"])
def api_stores_list(request):
    """List all stores (public) or create a new store (vendors only)."""
    if request.method == "GET":
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_is_vendor(request.user):
            return Response(
                {
                    "error": (
                        "Forbidden: Only registered vendors can create stores."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_vendor_stores(request, vendor_id):
    """List all stores associated with a specific vendor ID."""
    vendor = get_object_or_404(User, id=vendor_id)
    stores = Store.objects.filter(vendor=vendor)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def api_store_products(request, store_id):
    """List products of a store or add a product (store owner only)."""
    store = get_object_or_404(Store, id=store_id)

    if request.method == "GET":
        products = Product.objects.filter(store=store)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required to add products."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if store.vendor != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to modify this store."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(store=store)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_store_reviews(request, store_id):
    """Retrieve all product reviews for a given store (owner only)."""
    store = get_object_or_404(Store, id=store_id)

    if store.vendor != request.user and not request.user.is_staff:
        return Response(
            {"error": "Forbidden: You are not the owner of this store."},
            status=status.HTTP_403_FORBIDDEN,
        )

    reviews = Review.objects.filter(product__store=store)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
