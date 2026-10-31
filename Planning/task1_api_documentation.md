# eCommerce REST API Documentation & Architecture

This document outlines the API specifications, architectural constraints, and interaction sequence diagrams for the eCommerce REST API implementation (Practical Task 1).

---

## 1. Architectural Principles & Data Representations

The API is built using the **Django REST Framework (DRF)** adhering to RESTful architecture constraints:
* **Statelessness:** No client session state is stored on the server between API requests. Each request carries all necessary authentication headers and data payloads.
* **Uniform Interface & Resource Identification:** Resources (`stores`, `products`, `reviews`) are addressed via clear, predictable URIs.
* **Payload Representation:** JSON (JavaScript Object Notation) is used as the primary interchange format for all request bodies and response payloads.
* **Authentication & Permissions:** Sensitive vendor operations require HTTP Basic Authentication (`BasicAuthentication`) and an authenticated user session (`IsAuthenticated`). Store ownership checks ensure vendors can only modify their own resources.

---

## 2. API Endpoints Specification

### A. Store Endpoints

#### 1. List All Stores
* **Endpoint:** `GET /ecommerce/api/stores/`
* **Access:** Public (Buyers & Vendors)
* **Response Status:** `200 OK`
* **Response Payload Example:**
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
