from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import random

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["logistics"]

shipments_col = db["shipments"]
drivers_col = db["drivers"]

# Clear existing data
shipments_col.delete_many({})
drivers_col.delete_many({})
print("Cleared existing data")

# ── Config ──────────────────────────────────────────────
WAREHOUSES = ["BLR_01", "BLR_02", "MUM_01", "DEL_01", "HYD_01"]
SENDERS = ["Amazon", "Flipkart", "Meesho", "Nykaa", "Zomato", "IKEA", "Nike", "Apple"]
RECEIVERS = ["Darshan", "Arjun", "Priya", "Riya", "Kiran", "Sneha", "Rohan", "Meera"]
VEHICLES = ["bike", "truck", "van"]
DRIVER_NAMES = [
    "Rajesh Kumar", "Suresh Nair", "Anil Singh", "Vijay Menon",
    "Deepak Rao", "Manoj Patil", "Ramesh Verma", "Sunil Joshi",
    "Pramod Hegde", "Ganesh Iyer"
]
STATUSES = ["created", "in_transit", "out_for_delivery", "delivered", "returned"]

# Bangalore area coordinates (lng, lat)
BASE_COORDS = [77.59, 12.97]

def random_coords():
    return [
        round(BASE_COORDS[0] + random.uniform(-0.5, 0.5), 4),
        round(BASE_COORDS[1] + random.uniform(-0.5, 0.5), 4)
    ]

def past(days=0, hours=0):
    return datetime.utcnow() - timedelta(days=days, hours=hours)

# ── Seed Drivers ─────────────────────────────────────────
drivers = []
for i, name in enumerate(DRIVER_NAMES):
    driver = {
        "_id": f"DRV_{i+1:03}",
        "name": name,
        "vehicle": random.choice(VEHICLES),
        "status": random.choice(["searching", "assigned", "offline"]),
        "location": {
            "type": "Point",
            "coordinates": random_coords()
        }
    }
    drivers.append(driver)

drivers_col.insert_many(drivers)
print(f"Inserted {len(drivers)} drivers")

# ── Seed Shipments ────────────────────────────────────────
shipments = []
driver_ids = [d["_id"] for d in drivers]

for i in range(50):
    shipment_id = f"SHP_{i+1:04}"
    dispatched = past(days=random.randint(1, 30))
    estimated = dispatched + timedelta(days=random.randint(2, 7))
    warehouse = random.choice(WAREHOUSES)
    status_sequence = STATUSES[:random.randint(1, len(STATUSES))]

    # Build status logs
    status_logs = []
    ts = dispatched
    for s in status_sequence:
        status_logs.append({
            "status": s,
            "ts": ts
        })
        ts += timedelta(hours=random.randint(3, 24))

    final_status = status_sequence[-1]

    # Assign driver only if not delivered/returned
    assigned_driver = None
    if final_status in ["in_transit", "out_for_delivery", "assigned"]:
        assigned_driver = random.choice(driver_ids)

    # Return info for returned shipments
    return_info = None
    if final_status == "returned":
        return_info = {
            "reason": random.choice(["damaged", "wrong_item", "not_needed"]),
            "initiated_at": ts,
            "status": "initiated"
        }

    shipment = {
        "_id": shipment_id,
        "meta": {
            "sender": random.choice(SENDERS),
            "receiver": random.choice(RECEIVERS)
        },
        "outbound": {
            "warehouse_id": warehouse,
            "dispatched_at": dispatched.isoformat(),
            "estimated_delivery": estimated.isoformat()
        },
        "current_location": {
            "type": "Point",
            "coordinates": random_coords()
        },
        "status_logs": status_logs,
        "driver_id": assigned_driver,
        "return_info": return_info
    }
    shipments.append(shipment)

shipments_col.insert_many(shipments)
print(f"Inserted {len(shipments)} shipments")

# ── Summary ───────────────────────────────────────────────
print("\n── Seed Summary ──")
print(f"Drivers:   {drivers_col.count_documents({})}")
print(f"Shipments: {shipments_col.count_documents({})}")
print(f"  created:          {shipments_col.count_documents({'status_logs': {'$elemMatch': {'status': 'created'}}})}")
print(f"  in_transit:       {shipments_col.count_documents({'status_logs.status': 'in_transit'})}")
print(f"  out_for_delivery: {shipments_col.count_documents({'status_logs.status': 'out_for_delivery'})}")
print(f"  delivered:        {shipments_col.count_documents({'status_logs.status': 'delivered'})}")
print(f"  returned:         {shipments_col.count_documents({'return_info': {'$ne': None}})}")
print(f"  unassigned:       {shipments_col.count_documents({'driver_id': None})}")
print(f"  assigned:         {shipments_col.count_documents({'driver_id': {'$ne': None}})}")