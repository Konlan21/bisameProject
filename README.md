# 🛒 FastAPI Product Management System with Role-Based Access

This project implements a product management API using **FastAPI** with:

- Role-based access control (Vendor, Customer, Admin, etc.)
- JWT Authentication (Access & Refresh tokens)
- MongoDB integration (via MongoDB Atlas)
- Vendor-specific permissions for managing products
- Search, Filter, and Pagination
- Rate limiting to protect sensitive endpoints
- Unit tests using Pytest

---

## 🔧 Tech Stack

- **FastAPI** for building APIs
- **MongoDB Atlas** for cloud database
- **Pydantic v2** for request/response models
- **Pytest** for automated tests
- **slowapi** for rate limiting

---

## 🔐 User Roles

- `vendor`: Can create, view, update, and delete *their own* products.
- `customer`: Can search and view products.
- `admin/staff`: Can manage all products (extension ready).
- `banned/inactive`: Cannot log in.

---

## 🚀 Features

- ✅ JWT Login and Refresh Token Flow
- ✅ Vendor-restricted product creation and update
- ✅ Filtering, Searching, and Pagination
- ✅ Role-checking decorators
- ✅ MongoDB cloud connection
- ✅ Rate limiting for `/auth/login`, `/auth/refresh`, and key endpoints
- ✅ Pytest coverage for authentication and product routes

---

## ▶️ Running the Project

### 1. Clone the repo

```bash
git clone https://github.com/your-username/fastapi-product-system.git
cd fastapi-product-system
````
### 2. Setup Venv
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Setup up env vairiables in the .env file
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/dbname
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256

### Run the server
uvicorn main:app --reload
Visit  http://localhost:8000/docs for documentation

### Running tests
pytest tests/
