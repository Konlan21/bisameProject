
from db.mongo import affiliate_links, commissions_collection
from bson import ObjectId
from datetime import datetime


DIRECT_COMMISSION = 0.025
INDIRECT_COMMISSION = 0.0075


async def process_commissions(order_user_id: str, order_id: str, amount: float):
    # Find who referred this user
    link = await affiliate_links.find_one({"user_id": ObjectId(order_user_id)})
    if not link:
        return

    # Direct affiliate
    direct_affiliate = link.get("referred_by")
    if direct_affiliate:
        direct_commission = amount * DIRECT_COMMISSION
        await commissions_collection.insert_one({
            "user_id": direct_affiliate,
            "order_id": ObjectId(order_id),
            "level": "direct",
            "amount": direct_commission,
            "date": datetime.utcnow().isoformat()
        })

        # Check if there's an indirect affiliate
        indirect_link = await affiliate_links.find_one({"user_id": direct_affiliate})
        if indirect_link and indirect_link.get("referred_by"):
            indirect_affiliate = indirect_link.get("referred_by")
            indirect_commission = amount * INDIRECT_COMMISSION
            await commissions_collection.insert_one({
                "user_id": indirect_affiliate,
                "order_id": ObjectId(order_id),
                "level": "indirect",
                "amount": indirect_commission,
                "date": datetime.utcnow().isoformat()
            })