from app.config.db import drivers_collection
from app.models.driver import driver_template

def get_all_drivers():
    return list(drivers_collection.find({}))

def create_driver(data):
    driver = driver_template(data)
    drivers_collection.insert_one(driver)
    return driver

def update_driver_location(data):
    drivers_collection.update_one(
        {"_id": data["id"]},
        {"$set": {"location": data["location"]}}
    )
    from app.services.shipment_service import sync_shipment_with_driver
    sync_shipment_with_driver(data["id"])
    return {"message": "Driver location updated + shipment synced"}

def find_nearest_driver(coordinates):
    drivers = drivers_collection.find({
        "status": "searching",
        "vehicle": "truck",
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": coordinates},
                "$maxDistance": 10000
            }
        }
    }).limit(1)
    return list(drivers)