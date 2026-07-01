from app.config.db import shipments_collection, drivers_collection
from app.models.shipment import shipment_template
from datetime import datetime

def get_all_shipments():
    return list(shipments_collection.find({}))

def create_shipment(data):
    shipment = shipment_template(data)
    shipments_collection.insert_one(shipment)
    return shipment

def update_shipment_location(data):
    shipments_collection.update_one(
        {"_id": data["id"]},
        {
            "$set": {"current_location": data["location"]},
            "$push": {"status_logs": {"status": data["status"], "ts": datetime.utcnow()}}
        }
    )
    return {"message": "Shipment updated"}

def get_shipment(shipment_id):
    return shipments_collection.find_one({"_id": shipment_id})

def assign_driver(shipment_id):
    from app.services.driver_service import find_nearest_driver
    shipment = shipments_collection.find_one({"_id": shipment_id})
    if not shipment:
        return {"error": "Shipment not found"}
    coordinates = shipment["current_location"]["coordinates"]
    drivers = find_nearest_driver(coordinates)
    if not drivers:
        return {"message": "No drivers available"}
    driver = drivers[0]
    shipments_collection.update_one({"_id": shipment_id}, {"$set": {"driver_id": driver["_id"]}})
    drivers_collection.update_one({"_id": driver["_id"]}, {"$set": {"status": "assigned"}})
    return {"message": "Driver assigned", "driver": driver}

def sync_shipment_with_driver(driver_id):
    driver = drivers_collection.find_one({"_id": driver_id})
    if not driver:
        return
    shipment = shipments_collection.find_one({"driver_id": driver_id})
    if not shipment:
        return
    shipments_collection.update_one(
        {"_id": shipment["_id"]},
        {"$set": {"current_location": driver["location"]}}
    )

def initiate_return(data):
    shipments_collection.update_one(
        {"_id": data["id"]},
        {"$set": {"return_info": {"reason": data["reason"], "initiated_at": datetime.utcnow(), "status": "initiated"}}}
    )
    return {"message": "Return initiated"}