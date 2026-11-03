# eCommerce_app Django Project

Live Repository: [https://github.com/arianmalayery-studio/eCommerce_App.git](https://github.com/arianmalayery-studio/eCommerce_App.git)

This is a full-stack Django eCommerce platform featuring role-based authentication, tiered store and product browsing, consolidated vendor review management, Django REST Framework (DRF) APIs, and live Reddit API integration.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Key Entry Points & Navigation](#key-entry-points--navigation)
- [REST API Endpoints & Postman Usage](#rest-api-endpoints--postman-usage)
- [Third-Party API Integration (Reddit Feed)](#third-party-api-integration-reddit-feed)
- [Password Reset Testing](#password-reset-testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.12 or later installed. [Download Python](https://www.python.org/downloads/)
* MariaDB or MySQL installed and running locally on port `3306`.
* Git installed to clone the repository.
* Postman installed for testing RESTful API endpoints.

---

## Installation

1. **Clone the repository and enter the project folder:**

   ```bash
   git clone https://github.com/arianmalayery-studio/eCommerce_App.git
   cd eCommerce_app
   ```

2. **Create and activate a virtual environment:**

   * Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

   * macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install all dependencies:**

   *(All necessary packages, including `mysqlclient`, Django, DRF, and `requests`, are defined in `requirements.txt`)*

   ```bash
   pip install -r requirements.txt
   ```

---

## Database Setup

1. **Create MariaDB / MySQL database:**

   Run the following command in PowerShell to initialize a clean database:

   ```powershell
   mariadb -u root -p -e "DROP DATABASE IF EXISTS ecommerce_db; CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   ```

2. **Update database credentials in configuration settings** if your MySQL username or password differ:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'ecommerce_db',
           'USER': 'root',
           'PASSWORD': '<your_mysql_password>',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```

---

## Running the Project

1. **Apply migrations:**

   ```bash
   python manage.py makemigrations eCommerce
   python manage.py makemigrations grabsomore
   python manage.py migrate
   ```

2. **Create a superuser / vendor account:**

   ```bash
   python manage.py createsuperuser
   ```

3. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

4. **Access the application:**

   * Web Portal: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Key Entry Points & Navigation

The platform provides structured, noise-free browsing tiers for buyers and vendors:

* **Buyer Storefronts Directory (`/ecommerce/stores/`)**:
  Lists all active stores without dumping the entire multi-store product catalog on one screen. Clicking any store routes directly to that specific store's inventory.
* **Store Product Catalog (`/ecommerce/stores/<id>/products/`)**:
  Displays only items belonging to the chosen store.
* **Vendor Reviews Central (`/ecommerce/vendor/reviews/`)**:
  Aggregates all reviews across all products owned by the vendor into a single consolidated table.
* **Vendor Dashboard (`/ecommerce/dashboard/`)**:
  Storefront management portal for creating stores, editing profiles, and launching individual inventory managers.
* **Reddit Public Feed (`/ecommerce/reddit/`)**:
  Accessible directly from the "Reddit Feed" link in the top navigation bar.

---

## REST API Endpoints & Postman Usage

Test the RESTful API endpoints in Postman using **Basic Auth** (superuser/vendor credentials) and raw **JSON** payloads. Always include trailing slashes on endpoints.

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/ecommerce/api/stores/` | Public | List all registered stores |
| **POST** | `/ecommerce/api/stores/` | Vendor (Auth) | Create a new storefront |
| **GET** | `/ecommerce/api/vendors/<vendor_id>/stores/` | Public | List stores owned by a specific vendor |
| **GET** | `/ecommerce/api/stores/<store_id>/products/` | Public | View all products belonging to a store |
| **POST** | `/ecommerce/api/stores/<store_id>/products/` | Store Owner | Add a new product to a store |
| **GET** | `/ecommerce/api/stores/<store_id>/reviews/` | Store Owner | View customer reviews for a store's products |

### Example Product Payload (`POST /ecommerce/api/stores/1/products/`)
```json
{
  "name": "Mechanical Keyboard",
  "description": "Tactile switches with customizable RGB",
  "price": "129.99",
  "stock": 20
}
```

---

## Third-Party API Integration (Reddit Feed)

The application consumes Reddit's public feed using Python's `requests` library via `eCommerce/functions/reddit.py`:
* Accessible via the top navbar link or directly at [http://127.0.0.1:8000/ecommerce/reddit/](http://127.0.0.1:8000/ecommerce/reddit/).
* Displays post titles, author tags, and outbound thread links.
* Includes fallback mock handling to ensure page uptime if external requests are throttled.

---

## Password Reset Testing

For local password reset testing using the console backend:

1. Ensure the email backend is set to console in the settings file:
   ```python
   EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
   ```
2. Navigate to `http://127.0.0.1:8000/request-password-reset/` and submit an account email.
3. The password reset URL with the generated token prints directly to the running terminal console.

---

## Troubleshooting

* **Missing Trailing Slashes on API Requests:**
  Django REST Framework endpoints require trailing slashes (e.g., `/ecommerce/api/stores/`). Omitting the trailing slash causes 301 redirects that drop POST payloads.
* **Database Connection Issues:**
  Ensure the MariaDB service is active and the port and password in your settings match your local database configuration.

---

## Project Structure

```
eCommerce_app/
├── eCommerce_app/           # Project configuration package
│   ├── settings.py          # Database credentials, DRF, and app definitions
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── grabsomore/              # Authentication & user profile app
│   ├── models.py            # User and token models
│   ├── views.py             # Login, register, and reset views
│   ├── templates/           # Authentication templates
│   └── urls.py              # Auth URL routing
├── eCommerce/               # Storefront & REST API app
│   ├── api_views.py         # DRF REST endpoint views (stores, products, reviews)
│   ├── serializers.py       # DRF model serializers
│   ├── models.py            # Store, Product, Review, Order models
│   ├── views.py             # Frontend store views, vendor reviews, Reddit feed
│   ├── functions/
│   │   └── reddit.py        # Third-party Reddit API consumer
│   ├── templates/           # eCommerce & Reddit templates
│   │   └── eCommerce/
│   │       ├── base.html
│   │       ├── stores_list.html
│   │       ├── store_products.html
│   │       ├── vendor_reviews.html
│   │       ├── vendor_dashboard.html
│   │       └── reddit_feed.html
│   └── urls.py              # Store and API URL routing
├── Planning/                # Architecture diagrams and task documentation
│   ├── task1_api_documentation.md
│   ├── task2_research.md
│   ├── sequence_diagram.md
│   ├── sequence_diagram.txt
│   └── crud_matrix.txt
├── .gitignore               # Excludes venv, pycache, and local DBs
├── manage.py                # Django CLI utility
├── requirements.txt         # Project dependencies (including mysqlclient)
└── readme.md                # Project documentation
```