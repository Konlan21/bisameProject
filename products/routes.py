from fastapi import APIRouter, Depends, HTTPException, Response, Request
# from auth.dependencies import get_current_user
from auth.models import User
from roles.permissions import require_role
from products.models import Product
from fastapi import Query
from products.store import get_products_by_vendor
from products.store import get_products_by_vendor
from db.mongo import product_collection
from products.schemas import ProductDBModel, ProductCreateModel, ProductUpdateModel
from bson import ObjectId
from typing import List, Optional
from rate_limiter import limiter


router = APIRouter()


@router.post("/", response_model=ProductDBModel)
@limiter.limit("3/minute") 
async def create_product(request: Request, product: ProductCreateModel, user: User = Depends(require_role("vendor"))):
    product_dict = product.model_dump()
    product_dict["vendor"] = user.username
    result = await product_collection.insert_one(product_dict)
    saved = await product_collection.find_one({"_id": result.inserted_id})
    saved["_id"] = str(saved["_id"])
    return saved


@router.get("/mine")
async def list_my_products(
    user: User = Depends(require_role("vendor")),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    total = await product_collection.count_documents({"vendor": user.username})
    cursor = product_collection.find({"vendor": user.username}).skip(skip).limit(limit)
    products = []
    async for product in cursor:
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        products.append(product)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "products": products
    }




@router.put("/{id}", response_model=ProductDBModel)
async def update_product(
    id: str,
    product_data: ProductUpdateModel,
    user: User = Depends(require_role("vendor"))
):
    existing = await product_collection.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    if existing["vendor"] != user.username:
        raise HTTPException(status_code=403, detail="You can only update your own products")

    update_fields = {k: v for k, v in product_data.model_dump().items() if v is not None}
    await product_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

    updated = await product_collection.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return ProductDBModel(**updated)


@router.delete("/{id}", status_code=204)
@limiter.limit("3/minute")
async def delete_product(
    request: Request,
    id: str,
    user: User = Depends(require_role("vendor"))
):
    existing = await product_collection.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    if existing["vendor"] != user.username:
        raise HTTPException(status_code=403, detail="You can only delete your own products")

    await product_collection.delete_one({"_id": ObjectId(id)})
    return Response(status_code=204)


# product search
@router.get("/search", response_model=List[ProductDBModel])
@limiter.limit("10/minute")
async def search_products(
    request: Request,
    name: Optional[str] = Query(None),
    vendor: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if vendor:
        query["vendor"] = vendor
    if q:
        query["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]

    cursor = product_collection.find(query).skip(skip).limit(limit)
    results = []
    async for product in cursor:
        product["_id"] = str(product["_id"])
        results.append(ProductDBModel(**product))

    return results
