def driver_template(data):
    return {
        "_id": data.get("id"),
        "name": data.get("name"),
        "vehicle": data.get("vehicle"),
        "status": "searching",
        "location": {
            "type": "Point",
            "coordinates": data.get("coordinates", [0, 0])
        }
    }