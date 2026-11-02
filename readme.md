# AuthLog Django Project

This is a Django web application project that includes two main apps:

* **grabsomore**: Handles user authentication, registration, password reset, and user sessions.
* **eCommerce**: eCommerce functionality with products, storefront permissions, shopping cart, RESTful APIs (Django REST Framework), and Reddit API integration.

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [REST API Endpoints & Postman Usage](#rest-api-endpoints--postman-usage)
- [Third-Party API Integration (Reddit Feed)](#third-party-api-integration-reddit-feed)
- [Password Reset Testing](#password-reset-testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.12 or later installed. [Download Python](https://www.python.org/downloads/)
* MariaDB or MySQL installed and running on your machine (default port 3306).
* Basic knowledge of using the command line / terminal.
* Git installed to clone the repository.
* Postman installed for testing RESTful API endpoints.

---

## Installation

1. **Clone the repository:**

   Clone the repository to your local machine and navigate into the project directory:

   ```bash
   git clone https://github.com/arianmalayery-studio/eCommerce_App.git
   cd AuthLog
   ```

2. **Create and activate a virtual environment:**

   Create the virtual environment directly inside the cloned project directory:

   * On Windows (PowerShell):

     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Email Settings:**

   For local password reset testing, ensure the console backend is configured in `AuthLog/settings.py`:

   ```python
   EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
   ```

---

## Database Setup

1. **Create MariaDB / MySQL database:**

   Run the following command in PowerShell to create a clean database:

   ```powershell
   mariadb -u root -p -e "DROP DATABASE IF EXISTS ecommerce_db; CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   ```

   *(Alternatively, log into your MariaDB prompt using `mariadb -u root -p` and execute: `DROP DATABASE IF EXISTS ecommerce_db; CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`)*

2. **Update database credentials in `AuthLog/settings.py`** if your MySQL username or password differ:

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

3. **Install MySQL Python adapter** if not already installed:

   ```bash
   pip install mysqlclient
   ```

---

## Running the Project

1. **Apply migrations:**

   Run the following commands to create all necessary database tables:

   ```bash
   python manage.py makemigrations eCommerce
   python manage.py makemigrations grabsomore
   python manage.py migrate
   ```

2. **Create a superuser** (for admin access and vendor API testing):

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to enter a username, email, and password.

3. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

4. **Access the application:**

   * Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * You can login, register new accounts, browse storefronts, manage products, view the Reddit integration feed, and test password reset workflows.

---

## Usage

* **Authentication (`grabsomore` app):**

  * Login at `/` (root URL)
  * Register at `/register/`
  * Request password reset at `/request-password-reset/`
  * Reset password via token printed to the terminal console

* **eCommerce (`eCommerce` app):**

  * Browse product catalog at `/ecommerce/`
  * Vendor store management at `/ecommerce/vendor-dashboard/`
  * Reddit external feed at `/ecommerce/reddit/`
  * Add products to cart and checkout orders

---

## REST API Endpoints & Postman Usage

Test the RESTful API endpoints in Postman using **Basic Auth** (superuser credentials) and raw **JSON** payloads. Always include trailing slashes on endpoints.

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/ecommerce/api/stores/` | Public | Retrieve all registered stores |
| **POST** | `/ecommerce/api/stores/` | Vendor (Auth) | Create a new storefront |
| **GET** | `/ecommerce/api/vendors/<vendor_id>/stores/` | Public | List stores owned by a vendor |
| **GET** | `/ecommerce/api/stores/<store_id>/products/` | Public | View all products belonging to a store |
| **POST** | `/ecommerce/api/stores/<store_id>/products/` | Store Owner | Add a new product to the store |
| **GET** | `/ecommerce/api/stores/<store_id>/reviews/` | Store Owner | View customer reviews for store products |

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
* Accessible at [http://127.0.0.1:8000/ecommerce/reddit/](http://127.0.0.1:8000/ecommerce/reddit/).
* Displays post titles, author tags, and outbound thread links.
* Includes resilient fallback logic to ensure page availability if third-party endpoints rate-limit or challenge requests.

---

## Password Reset Testing

If you want to test password reset functionality without sending real emails:

1. Verify the email backend in `AuthLog/settings.py` is set to console:

   ```python
   EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
   ```

2. When you submit a password reset request at `/request-password-reset/`, the reset link will print in your console/terminal.

3. Copy and paste the link into your browser to reset the password.

---

## Troubleshooting

* **MySQL Client Missing Error:**

  If you get `ModuleNotFoundError: No module named 'mysqlclient'`, install it with:

  ```bash
  pip install mysqlclient
  ```

* **Database Table Missing Error (`1146`):**

  If tables are missing, ensure `ecommerce_db` was created and run:

  ```bash
  python manage.py migrate
  ```

* **Missing Trailing Slashes on API Requests:**

  Django REST Framework endpoints strictly expect trailing slashes (e.g., `/ecommerce/api/stores/`). Omitting the trailing slash can cause 301 redirects that drop POST payloads.

* **Static files not loading:**

  During development, Django serves static files automatically. For production, you need to configure static files properly.

---

## Project Structure

```
AuthLog/
├── AuthLog/
│   ├── settings.py          # Project settings (DB, DRF, email, apps)
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── grabsomore/              # Authentication app
│   ├── models.py            # User and token models
│   ├── views.py             # Login, register, and reset views
│   ├── templates/           # Authentication templates
│   │   └── grabsomore/
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── request_password_reset.html
│   │       └── password_reset.html
│   └── urls.py              # Auth URL routing
├── eCommerce/               # eCommerce app
│   ├── api_views.py         # DRF REST endpoint views
│   ├── serializers.py       # DRF model serializers
│   ├── models.py            # Store, Product, Review, Order models
│   ├── views.py             # Front-end store views & Reddit feed view
│   ├── functions/
│   │   └── reddit.py        # Third-party Reddit API consumer
│   ├── templates/           # eCommerce & Reddit templates
│   │   └── eCommerce/
│   │       ├── base.html
│   │       ├── products_list.html
│   │       ├── vendor_dashboard.html
│   │       └── reddit_feed.html
│   └── urls.py
├── Planning/                # Architecture and task documentation
│   ├── task1_api_documentation.md
│   ├── task2_research.md
│   └── sequence_diagram.md
├── manage.py                # Django CLI utility
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---