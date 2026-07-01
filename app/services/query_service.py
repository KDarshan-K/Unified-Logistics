import os
import json
from groq import Groq
from app.config.db import db

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an expert MongoDB query generator for a logistics platform.
The database has two collections:

shipments: {
    _id: string,
    meta: { sender: string, receiver: string },
    outbound: { warehouse_id: string, dispatched_at: string, estimated_delivery: string },
    current_location: { type: "Point", coordinates: [lng, lat] },
    status_logs: [{ status: string, ts: datetime }],
    driver_id: string or null,
    return_info: { reason: string, status: string, initiated_at: datetime } or null
}

drivers: {
    _id: string,
    name: string,
    vehicle: string (bike/truck/van),
    status: string (searching/assigned/offline),
    location: { type: "Point", coordinates: [lng, lat] }
}

The user will ask a natural language question. You must respond ONLY with a valid JSON object like this:
{
    "collection": "shipments",
    "pipeline": [
        { "$match": { ... } },
        { "$group": { ... } }
    ]
}

Rules:
- collection must be "shipments" or "drivers"
- pipeline must be a valid MongoDB aggregation pipeline array
- Do NOT include any explanation, markdown, or text outside the JSON
- For status queries, check status_logs array last element
- For unassigned shipments, check driver_id is null
"""

def run_natural_language_query(question: str):
    # Step 1 — Ask Groq to generate the pipeline
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    # Step 2 — Parse the JSON response
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "Could not parse LLM response",
            "raw": raw
        }

    collection_name = parsed.get("collection")
    pipeline = parsed.get("pipeline")

    if collection_name not in ["shipments", "drivers"]:
        return {"error": f"Invalid collection: {collection_name}"}

    if not isinstance(pipeline, list):
        return {"error": "Pipeline is not a list"}

    # Step 3 — Run the pipeline against real MongoDB
    try:
        collection = db[collection_name]
        results = list(collection.aggregate(pipeline))

        # Convert ObjectId/_id to string for JSON serialization
        for r in results:
            if "_id" in r and not isinstance(r["_id"], str):
                r["_id"] = str(r["_id"])

        return {
            "question": question,
            "collection": collection_name,
            "pipeline": pipeline,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        return {
            "error": str(e),
            "pipeline": pipeline
        }