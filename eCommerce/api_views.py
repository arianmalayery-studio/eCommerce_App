"""API Views for eCommerce Task 1."""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Store, Product, Review
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer


@api_view(["GET", "POST"])
def api_stores_list(request):
    """List all stores (GET) or allow authenticated vendors to create a store (POST)."""
    if request.method == "GET":
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the store vendor to the authenticated user
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_vendor_stores(request, vendor_id):
    """Retrieve all stores owned by a specific vendor."""
    stores = Store.objects.filter(vendor_id=vendor_id)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def api_store_products(request, store_id):
    """Retrieve products of a store (GET) or add a product to a store (POST)."""
    store = get_object_or_404(Store, pk=store_id)

    if request.method == "GET":
        products = Product.objects.filter(store=store)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required to add products."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Enforce that only the store's vendor owner can add products
        if store.vendor != request.user:
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
    """Allow vendors to retrieve reviews for their own store."""
    store = get_object_or_404(Store, pk=store_id)

    # Vendor ownership check
    if store.vendor != request.user:
        return Response(
            {"error": "Forbidden: You are not the owner of this store."},
            status=status.HTTP_403_FORBIDDEN,
        )

    reviews = Review.objects.filter(store=store)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
