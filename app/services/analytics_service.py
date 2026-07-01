from app.config.db import shipments_collection

def returns_by_warehouse():
    pipeline = [
        {"$match": {"return_info.reason": "damaged"}},
        {"$group": {"_id": "$outbound.warehouse_id", "total_returns": {"$sum": 1}}},
        {"$sort": {"total_returns": -1}}
    ]
    return list(shipments_collection.aggregate(pipeline))