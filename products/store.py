from products.models import Product
from db.mongo import product_collection

product_store = []
product_id_customer = 1


def add_product(product: Product):
    global product_id_customer
    product.id = product_id_customer
    product_store.append(product)
    product_id_customer += 1
    return product


def get_all_products():
    return product_store



async def get_products_by_vendor(vendor_username: str):
    cursor = product_collection.find({"vendor": vendor_username})
    products = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to str
        products.append(doc)
    return products

