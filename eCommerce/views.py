"""Views for the eCommerce catalog, cart, and vendor storefront management."""

from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .functions.reddit import get_reddit_posts
from .models import Order, OrderItem, Product, Review, Store
from .serializers import ProductSerializer, ReviewSerializer, StoreSerializer

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def check_is_vendor(user):
    """Check if the authenticated user has Vendor or Superuser status."""
    return user.is_authenticated and (
        user.groups.filter(name="Vendors").exists() or user.is_superuser
    )


# ==============================================================================
# CATALOG & STORE BROWSING (BUYER & GENERAL)
# ==============================================================================


def stores_list(request):
    """Entry point: list all stores so buyers can browse stores first."""
    stores = Store.objects.all().select_related("vendor")
    is_vendor = check_is_vendor(request.user)
    return render(
        request,
        "eCommerce/stores_list.html",
        {"stores": stores, "is_vendor": is_vendor},
    )


def store_products(request, store_id):
    """Display only products belonging to the selected store."""
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    is_vendor = check_is_vendor(request.user)
    return render(
        request,
        "eCommerce/store_products.html",
        {"store": store, "products": products, "is_vendor": is_vendor},
    )


def products_list(request):
    """Render public catalog of available products across all stores."""
    products = Product.objects.all().select_related("store")
    is_vendor = check_is_vendor(request.user)
    return render(
        request,
        "eCommerce/products_list.html",
        {"products": products, "is_vendor": is_vendor},
    )


def product_page(request, product_id):
    """Display detailed product view with review submission and history."""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by("-created_at")
    is_vendor = check_is_vendor(request.user)
    return render(
        request,
        "eCommerce/product_page.html",
        {"product": product, "reviews": reviews, "is_vendor": is_vendor},
    )


@login_required
def add_review(request, product_id):
    """Create verified or unverified review depending on purchase history."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        rating = int(request.POST.get("rating", 5))

        has_purchased = OrderItem.objects.filter(
            order__buyer=request.user, product=product
        ).exists()

        Review.objects.create(
            product=product,
            user=request.user,
            comment=comment,
            rating=rating,
            is_verified=has_purchased,
        )
    return redirect("eCommerce:product_page", product_id=product.id)


def add_to_cart(request, product_id):
    """Add requested quantity of product to session cart for buyers only."""
    if check_is_vendor(request.user):
        return HttpResponseForbidden("Vendors cannot purchase products.")

    quantity = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})
    str_id = str(product_id)
    cart[str_id] = cart.get(str_id, 0) + quantity
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("eCommerce:main_cart_page")


def update_cart_item(request, product_id):
    """Update item quantity or remove it if set to zero."""
    if check_is_vendor(request.user):
        return HttpResponseForbidden("Vendors cannot access cart.")

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get("cart", {})
        str_id = str(product_id)

        if quantity > 0:
            cart[str_id] = quantity
        else:
            cart.pop(str_id, None)

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("eCommerce:main_cart_page")


def remove_from_cart(request, product_id):
    """Remove line item from session cart."""
    if check_is_vendor(request.user):
        return HttpResponseForbidden("Vendors cannot access cart.")

    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("eCommerce:main_cart_page")


def main_cart_page(request):
    """Render shopping cart details; restricted to buyers."""
    if check_is_vendor(request.user):
        return HttpResponseForbidden("Vendors cannot purchase products.")

    cart = request.session.get("cart", {})
    cart_items = []
    total = Decimal("0.00")

    for prod_id, qty in cart.items():
        try:
            product = Product.objects.get(id=int(prod_id))
            subtotal = product.price * qty
            total += subtotal
            cart_items.append(
                {"product": product, "quantity": qty, "subtotal": subtotal}
            )
        except Product.DoesNotExist:
            continue

    return render(
        request,
        "eCommerce/main_cart_page.html",
        {"cart_items": cart_items, "total": total, "is_vendor": False},
    )


@login_required
def checkout(request):
    """Finalize order, decrement stock, email invoice, and clear cart."""
    if check_is_vendor(request.user):
        return HttpResponseForbidden("Vendors cannot check out.")

    cart = request.session.get("cart", {})
    if not cart:
        return redirect("eCommerce:products_list")

    total = Decimal("0.00")
    order = Order.objects.create(buyer=request.user, total_amount=0)
    invoice_lines = [
        "========================================",
        f"       INVOICE FOR ORDER #{order.id}",
        "========================================",
        f"Customer: {request.user.username}",
        f"Email:    {request.user.email}",
        "----------------------------------------",
        "Items:",
    ]

    for prod_id, qty in cart.items():
        product = get_object_or_404(Product, id=int(prod_id))
        if product.stock >= qty:
            product.stock -= qty
            product.save()

            line_total = product.price * qty
            total += line_total
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price_at_purchase=product.price,
            )
            invoice_lines.append(
                f"- {product.name} (x{qty}) @ " f"${product.price} =${line_total}"
            )

    order.total_amount = total
    order.save()
    invoice_lines.append("----------------------------------------")
    invoice_lines.append(f"TOTAL: ${total}")
    invoice_text = "\n".join(invoice_lines)

    if request.user.email:
        email = EmailMessage(
            subject=f"Invoice for Order #{order.id}",
            body=invoice_text,
            from_email="noreply@grabsomore.local",
            to=[request.user.email],
        )
        email.send()

    request.session["cart"] = {}
    request.session.modified = True

    return render(
        request,
        "eCommerce/checkout_success.html",
        {"order": order, "invoice": invoice_text, "is_vendor": False},
    )


# ==============================================================================
# VENDOR STORE CRUD & REVIEWS VIEW
# ==============================================================================


@login_required
def vendor_dashboard(request):
    """List storefronts owned by requesting vendor."""
    if not check_is_vendor(request.user):
        return HttpResponseForbidden("Access restricted to Vendors.")
    stores = request.user.stores.all()
    return render(
        request,
        "eCommerce/vendor_dashboard.html",
        {"stores": stores, "is_vendor": True},
    )


@login_required
def vendor_reviews(request):
    """Aggregated list of all reviews across all vendor products."""
    if not check_is_vendor(request.user):
        return HttpResponseForbidden("Access restricted to Vendors.")
    vendor_stores = request.user.stores.all()
    reviews = (
        Review.objects.filter(product__store__in=vendor_stores)
        .select_related("product", "product__store", "user")
        .order_by("-created_at")
    )
    return render(
        request,
        "eCommerce/vendor_reviews.html",
        {"reviews": reviews, "is_vendor": True},
    )


@login_required
def create_store(request):
    """Create new storefront associated with vendor."""
    if not check_is_vendor(request.user):
        return HttpResponseForbidden("Access restricted to Vendors.")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        Store.objects.create(vendor=request.user,
                             name=name, description=description)
        return redirect("eCommerce:vendor_dashboard")
    return render(
        request,
        "eCommerce/store_form.html",
        {"action": "Create", "is_vendor": True},
    )


@login_required
def edit_store(request, store_id):
    """Edit existing storefront owned by requesting vendor."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        store.name = request.POST.get("name")
        store.description = request.POST.get("description", "")
        store.save()
        return redirect("eCommerce:vendor_dashboard")
    return render(
        request,
        "eCommerce/store_form.html",
        {"store": store, "action": "Edit", "is_vendor": True},
    )


@login_required
def delete_store(request, store_id):
    """Remove storefront owned by requesting vendor."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        store.delete()
        return redirect("eCommerce:vendor_dashboard")
    return render(
        request,
        "eCommerce/confirm_delete.html",
        {"item": store, "type": "Store", "is_vendor": True},
    )


# ==============================================================================
# VENDOR PRODUCT CRUD
# ==============================================================================


@login_required
def add_product(request, store_id):
    """Create new product listing linked to vendor store."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        price = Decimal(request.POST.get("price"))
        stock = int(request.POST.get("stock"))
        Product.objects.create(
            store=store,
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        return redirect("eCommerce:store_products", store_id=store.id)
    return render(
        request,
        "eCommerce/product_form.html",
        {"store": store, "action": "Add", "is_vendor": True},
    )


@login_required
def edit_product(request, product_id):
    """Edit existing product details owned by requesting vendor."""
    product = get_object_or_404(
        Product, id=product_id, store__vendor=request.user)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description", "")
        product.price = Decimal(request.POST.get("price"))
        product.stock = int(request.POST.get("stock"))
        product.save()
        return redirect("eCommerce:store_products", store_id=product.store.id)
    return render(
        request,
        "eCommerce/product_form.html",
        {
            "product": product,
            "store": product.store,
            "action": "Edit",
            "is_vendor": True,
        },
    )


@login_required
def delete_product(request, product_id):
    """Remove product item owned by requesting vendor."""
    product = get_object_or_404(
        Product, id=product_id, store__vendor=request.user)
    store_id = product.store.id
    if request.method == "POST":
        product.delete()
        return redirect("eCommerce:store_products", store_id=store_id)
    return render(
        request,
        "eCommerce/confirm_delete.html",
        {"item": product, "type": "Product", "is_vendor": True},
    )


# ==============================================================================
# REST API ENDPOINTS & REDDIT FEED
# ==============================================================================


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

        if not check_is_vendor(request.user):
            return Response(
                {"error": ("Forbidden: Only registered vendors can create stores.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
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
    """Allow vendors to retrieve reviews for products belonging to their store."""
    store = get_object_or_404(Store, pk=store_id)

    if store.vendor != request.user:
        return Response(
            {"error": "Forbidden: You are not the owner of this store."},
            status=status.HTTP_403_FORBIDDEN,
        )

    reviews = Review.objects.filter(product__store=store)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def reddit_feed(request):
    """Fetch posts from Reddit and pass them to the template."""
    posts = get_reddit_posts("python")
    is_vendor = check_is_vendor(request.user)
    return render(
        request,
        "eCommerce/reddit_feed.html",
        {"posts": posts, "is_vendor": is_vendor},
    )
