# eCommerce Project Planning Document

## 1. System Requirements
* **Vendors:** Account registration in the Vendors group; full CRUD capabilities over digital storefronts (Store model) and inventory items (Product model).
* **Buyers:** Account registration in the Buyers group; cross-store product catalog browsing; session-backed multi-item cart management; checkout and invoicing; product review submissions.
* **Store Platform:** Session persistence; automated inventory deduction upon order confirmation; invoice dispatch via Django core mail; token-based single-use expiring password recovery.

## 2. User Interface Layout
* **Catalog (`products_list.html`):** Multi-column responsive grid displaying title, store affiliation, price, and stock levels. Role-based navigation toggles access to the Vendor Dashboard.
* **Product Detail (`product_page.html`):** Comprehensive item specs, quantity selection input, quick navigation shortcuts to cart, and chronological reviews list.
* **Shopping Cart (`main_cart_page.html`):** Tabular itemized summary with real-time subtotal calculation, order total display, and one-click checkout.
* **Vendor Dashboard (`vendor_dashboard.html`):** Storefront listing, inline product tables, and explicit action buttons for editing and removing resources.

## 3. Access Control & Data Security
* **Authentication:** Handled through Django's `django.contrib.auth` framework with salted PBKDF2/SHA-256 password hashing.
* **Role-Based Authorization:** Custom `Vendors` and `Buyers` groups restricting administrative and mutation views. Store and product modifications verify requesting vendor ownership (`vendor=request.user`) to prevent cross-account tampering.
* **Password Reset Security:** Ephemeral tokens hashed via SHA-1 in the database, restricted to a 5-minute validity window, and permanently deleted upon successful password change or expiration.

## 4. Failure Recovery & Error Handling
* **Out-of-Stock Conditions:** Checkout validates item stock before processing line items; prevents decrementing below zero.
* **Invalid Authentication / Session Expiry:** Graceful redirects with user-facing alerts on mismatched credentials or expired recovery links.
* **Database Connection Failures:** Unhandled exceptions caught through custom 404/500 handlers; sensitive database connection strings decoupled from template outputs.
