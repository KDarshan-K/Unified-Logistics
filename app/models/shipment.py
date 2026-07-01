def shipment_template(data):
    return {
        "_id": data.get("id"),
        "meta": {
            "sender": data.get("sender"),
            "receiver": data.get("receiver")
        },
        "outbound": {
            "warehouse_id": data.get("warehouse_id"),
            "dispatched_at": data.get("dispatched_at"),
            "estimated_delivery": data.get("estimated_delivery")
        },
        "current_location": {
            "type": "Point",
            "coordinates": [0, 0]
        },
        "status_logs": [
            {
                "status": "created",
                "ts": data.get("dispatched_at")
            }
        ],
        "return_info": None
    }