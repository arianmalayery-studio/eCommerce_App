# REST API Architecture Sequence Diagram

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
