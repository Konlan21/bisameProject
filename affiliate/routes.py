from fastapi import APIRouter, HTTPException
from affiliate.schemas import OrderModel
from db.mongo import orders_collection,  commissions_collection
from affiliate.logic import process_commissions
from bson import ObjectId

router = APIRouter()


#order placment logic
@router.post("/place-order")
async def place_order(order: OrderModel):
    try:
        # Save the order to MongoDB
        order_data = order.model_dump()
        result = await orders_collection.insert_one(order_data)
        order_id = result.inserted_id

        # process commisions
        await process_commissions(
            order_user_id=order.user,
            order_id=str(order_id),
            amount=order.amount
        )

        return {
            "message": "Order received and commission processed",
            "order_id": str(order_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order failed: {str(e)}")
