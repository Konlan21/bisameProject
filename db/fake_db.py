# db/fake_db.py
from auth.models import User
users_db = {
    "customer1": User(username="customer1", password="123", role="customer"),
    "vendor1": User(username="vendor1", password="123", role="vendor"),
    "vendor2": User(username="vendor2", password="121", role="vendor"),  # ✅ FIXED key
    "admin1": User(username="admin1", password="123", role="admin", is_active=True),
    "staff1": User(username="staff1", password="123", role="staff", is_active=True),
    "banned_user": User(username="banned_user", password="123", role="customer", is_banned=True),
}
