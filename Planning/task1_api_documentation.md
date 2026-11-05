# eCommerce REST API Documentation & Architecture

This document outlines the API specifications, architectural constraints, and interaction sequence diagrams for the eCommerce REST API implementation (Practical Task 1).

---

## 1. Architectural Principles & Data Representations

The API is built using the **Django REST Framework (DRF)** adhering to RESTful architecture constraints:
* **Statelessness:** No client session state is stored on the server between API requests. Each request carries all necessary authentication headers and data payloads.
* **Uniform Interface & Resource Identification:** Resources (`stores`, `products`, `reviews`) are addressed via clear, predictable URIs.
* **Payload Representation:** JSON (JavaScript Object Notation) is used as the primary interchange format for all request bodies and response payloads.
* **Authentication & Permissions:** Sensitive vendor operations require HTTP Basic Authentication (`BasicAuthentication`) and an authenticated user session (`IsAuthenticated`). Store ownership checks ensure vendors can only modify their own resources. Role checks ensure that only vendors and superusers can create storefronts.

---

## 2. Authentication & Headers

| Header | Value | Description |
| :--- | :--- | :--- |
| `Authorization` | `Basic <base64(user:pass)>` | Required on protected endpoints (Vendor/Owner operations) |
| `Content-Type` | `application/json` | Required for all `POST` / `PUT` / `PATCH` payloads |
| `Accept` | `application/json` | Expected response media type |

---

## 3. API Endpoints Overview

| Method | Endpoint | Authorization | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/ecommerce/api/stores/` | Public | List all storefronts |
| **POST** | `/ecommerce/api/stores/` | Vendor Only (`403` for Buyers) | Create a new storefront |
| **GET** | `/ecommerce/api/vendors/<vendor_id>/stores/` | Public | List stores owned by a specific vendor |
| **GET** | `/ecommerce/api/stores/<store_id>/products/` | Public | Retrieve all products belonging to a store |
| **POST** | `/ecommerce/api/stores/<store_id>/products/` | Store Owner Only | Add a new product to a store |
| **GET** | `/ecommerce/api/stores/<store_id>/reviews/` | Store Owner Only | View all reviews for a store's products |

---

## 4. Endpoint Specifications

### 4.1 List All Stores
* **Endpoint:** `GET /ecommerce/api/stores/`
* **Access Level:** Public
* **Response `200 OK`:**
```json
[
  {
    "id": 1,
    "vendor": 1,
    "vendor_username": "admin",
    "name": "Woodstock Tech Hub",
    "description": "Custom hardware, parts, and accessories"
  }
]
```

---

### 4.2 Create Store
* **Endpoint:** `POST /ecommerce/api/stores/`
* **Access Level:** Authenticated Vendor (`Vendors` group or Superuser)
* **Headers:** `Content-Type: application/json`, `Authorization: Basic <credentials>`
* **Request Payload:**
```json
{
  "name": "Woodstock Audio & Tech",
  "description": "High performance speakers and custom cables"
}
```
* **Response `201 Created`:**
```json
{
  "id": 2,
  "vendor": 1,
  "vendor_username": "admin",
  "name": "Woodstock Audio & Tech",
  "description": "High performance speakers and custom cables"
}
```
* **Response `401 Unauthorized`:**
```json
{
  "error": "Authentication credentials were not provided."
}
```
* **Response `403 Forbidden` (Buyer attempted store creation):**
```json
{
  "error": "Forbidden: Only registered vendors can create stores."
}
```
* **Response `400 Bad Request`:**
```json
{
  "name": [
    "This field is required."
  ]
}
```

---

### 4.3 List Stores by Vendor
* **Endpoint:** `GET /ecommerce/api/vendors/<vendor_id>/stores/`
* **Access Level:** Public
* **Response `200 OK`:**
```json
[
  {
    "id": 1,
    "vendor": 1,
    "vendor_username": "admin",
    "name": "Woodstock Tech Hub",
    "description": "Custom hardware, parts, and accessories"
  }
]
```

---

### 4.4 List Store Products
* **Endpoint:** `GET /ecommerce/api/stores/<store_id>/products/`
* **Access Level:** Public
* **Response `200 OK`:**
```json
[
  {
    "id": 1,
    "store": 1,
    "name": "Mechanical Keyboard",
    "description": "Hot-swappable tactile switches with RGB",
    "price": "129.99",
    "stock": 15
  }
]
```

---

### 4.5 Add Product to Store
* **Endpoint:** `POST /ecommerce/api/stores/<store_id>/products/`
* **Access Level:** Authenticated Store Owner Only
* **Headers:** `Content-Type: application/json`, `Authorization: Basic <credentials>`
* **Request Payload:**
```json
{
  "name": "Custom Coiled USB Cable",
  "description": "Double-sleeved aviator connector cable",
  "price": "34.50",
  "stock": 40
}
```
* **Response `201 Created`:**
```json
{
  "id": 2,
  "store": 1,
  "name": "Custom Coiled USB Cable",
  "description": "Double-sleeved aviator connector cable",
  "price": "34.50",
  "stock": 40
}
```
* **Response `401 Unauthorized`:**
```json
{
  "error": "Authentication required to add products."
}
```
* **Response `403 Forbidden` (User does not own store):**
```json
{
  "error": "You do not have permission to modify this store."
}
```
* **Response `400 Bad Request`:**
```json
{
  "price": [
    "A valid number is required."
  ]
}
```

---

### 4.6 Retrieve Store Reviews
* **Endpoint:** `GET /ecommerce/api/stores/<store_id>/reviews/`
* **Access Level:** Authenticated Store Owner Only (`BasicAuthentication` + `IsAuthenticated`)
* **Headers:** `Authorization: Basic <credentials>`
* **Response `200 OK`:**
```json
[
  {
    "id": 1,
    "product": 1,
    "user": 2,
    "rating": 5,
    "comment": "Exceptional build quality and fast shipping!",
    "is_verified": true,
    "created_at": "2026-11-04T12:00:00Z"
  }
]
```
* **Response `401 Unauthorized`:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```
* **Response `403 Forbidden` (Requester does not own the store):**
```json
{
  "error": "Forbidden: You are not the owner of this store."
}
```

---

## 5. Architectural Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / Postman
    participant Endpoint as Django REST API Endpoint
    participant Auth as Auth & Permission Layer
    participant Serializer as DRF Serializer
    participant DB as MariaDB Database

    Note over Client,DB: Flow 1: Create Store (Role-Restricted)
    Client->>Endpoint: POST /ecommerce/api/stores/ (Basic Auth + JSON)
    Endpoint->>Auth: Verify user.is_authenticated & check_is_vendor()
    alt Not Vendor / Buyer Role
        Auth-->>Client: 403 Forbidden {"error": "Only vendors can create stores"}
    else Is Vendor
        Endpoint->>Serializer: Validate payload (StoreSerializer)
        Serializer->>DB: INSERT INTO eCommerce_store
        DB-->>Serializer: Store record saved
        Serializer-->>Client: 201 Created (Store JSON)
    end

    Note over Client,DB: Flow 2: Retrieve Store Products (Public)
    Client->>Endpoint: GET /ecommerce/api/stores/{store_id}/products/
    Endpoint->>DB: SELECT * FROM eCommerce_product WHERE store_id = {store_id}
    DB-->>Endpoint: Product QuerySet
    Endpoint->>Serializer: Serialize QuerySet (ProductSerializer)
    Serializer-->>Client: 200 OK (Product List JSON)

    Note over Client,DB: Flow 3: Add Product to Store (Store Owner Only)
    Client->>Endpoint: POST /ecommerce/api/stores/{store_id}/products/ (Auth + JSON)
    Endpoint->>Auth: Check if request.user == store.vendor
    alt User is NOT store owner
        Auth-->>Client: 403 Forbidden {"error": "Permission denied"}
    else User is store owner
        Endpoint->>Serializer: Validate payload (ProductSerializer)
        Serializer->>DB: INSERT INTO eCommerce_product
        DB-->>Serializer: Product record saved
        Serializer-->>Client: 201 Created (Product JSON)
    end

    Note over Client,DB: Flow 4: Retrieve Store Reviews (Vendor Only)
    Client->>Endpoint: GET /ecommerce/api/stores/{store_id}/reviews/ (Basic Auth)
    Endpoint->>Auth: Verify BasicAuthentication & check request.user == store.vendor
    alt Not Store Owner
        Auth-->>Client: 403 Forbidden
    else Is Store Owner
        Endpoint->>DB: SELECT * FROM eCommerce_review WHERE product__store_id = {store_id}
        DB-->>Endpoint: Review QuerySet
        Endpoint->>Serializer: Serialize QuerySet (ReviewSerializer)
        Serializer-->>Client: 200 OK (Reviews JSON)
    end
```
