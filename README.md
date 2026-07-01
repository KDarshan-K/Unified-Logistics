#  Unified Logistics Hub

An AI-powered logistics and warehouse management platform with real-time shipment tracking, intelligent driver assignment, and a natural language admin query interface powered by Groq/Llama 3.1.

---

## Features

- **Shipment lifecycle management** — create, track, update, and return shipments with full status history
- **Driver assignment engine** — geo-based nearest driver lookup using MongoDB `$near` queries
- **Real-time tracking** — HTMX-powered live status polling on shipment detail pages (no JavaScript framework needed)
- **AI Admin Query Panel** — ask plain English questions; the system generates and executes MongoDB aggregation pipelines via Groq/Llama 3.1
- **Returns analytics** — warehouse-level return tracking with aggregation pipeline
- **Server-rendered frontend** — FastAPI + Jinja2 + Tailwind CSS, no build step required

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.12 |
| Database | MongoDB (PyMongo) |
| Frontend | Jinja2 Templates, Tailwind CSS (CDN), HTMX |
| AI / LLM | Groq API (Llama 3.1 8B Instant) |
| Config | python-dotenv |
| Server | Uvicorn |

---

## Project Structure

```
Unified-logistics/
├── app/
│   ├── main.py                  # FastAPI app, route registration, template mounting
│   ├── config/
│   │   └── db.py                # MongoDB connection, collection references
│   ├── models/
│   │   ├── shipment.py          # Shipment document template
│   │   └── driver.py            # Driver document template
│   ├── routes/
│   │   ├── shipment_routes.py   # Shipment CRUD + status fragment endpoint
│   │   ├── driver_routes.py     # Driver CRUD + location update
│   │   ├── analytics_routes.py  # Returns by warehouse
│   │   └── query_routes.py      # Admin NL query panel
│   ├── services/
│   │   ├── shipment_service.py  # Business logic — create, update, assign, return
│   │   ├── driver_service.py    # Business logic — create, locate, update
│   │   ├── analytics_service.py # Aggregation pipelines
│   │   └── query_service.py     # Groq LLM → MongoDB pipeline generation
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── shipments.html
│   │   ├── shipment_detail.html
│   │   ├── drivers.html
│   │   ├── admin.html
│   │   └── _status_fragment.html
│   └── static/                  # Static assets
├── seed.py                      # Seeds 50 shipments + 10 drivers into MongoDB
├── requirements.txt
└── .env
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB running locally or MongoDB Atlas connection string
- Groq API key ([console.groq.com](https://console.groq.com))

### Installation

```bash
git clone https://github.com/KDarshan-K/Unified-logistics.git
cd Unified-logistics
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the repo root:

```
MONGO_URI=###########################
GROQ_API_KEY=########################
```

### Seed the Database

Populate 50 realistic shipments across 5 warehouses and 10 drivers:

```bash
python seed.py
```

### Run the App

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000`

---

## Pages

| Route | Description |
|---|---|
| `/` | Dashboard — summary cards, recent shipments |
| `/shipments` | Full shipments table with status badges |
| `/shipments/{id}` | Shipment detail with live HTMX status refresh |
| `/drivers` | Driver list with vehicle type and status |
| `/admin` | AI-powered natural language query panel |

---

## API Endpoints

### Shipments

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/shipment/all` | List all shipments |
| `GET` | `/shipment/{id}` | Get single shipment |
| `POST` | `/shipment/create` | Create new shipment |
| `POST` | `/shipment/update` | Update location and status |
| `POST` | `/shipment/assign-driver` | Auto-assign nearest available driver |
| `POST` | `/shipment/return` | Initiate return |

### Drivers

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/driver/all` | List all drivers |
| `POST` | `/driver/create` | Register new driver |
| `POST` | `/driver/update-location` | Update driver location + sync shipment |

### Analytics

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/analytics/returns` | Returns grouped by warehouse |
| `POST` | `/admin/query` | Natural language → MongoDB pipeline |

---

## AI Admin Query Panel

The admin panel accepts plain English questions and uses Groq/Llama 3.1 to generate MongoDB aggregation pipelines, which are executed against live data and returned alongside the generated pipeline for full transparency.

**Example queries:**

- `How many shipments are unassigned?`
- `Which warehouse has the most returns?`
- `Count shipments by status`
- `How many drivers are currently searching?`
- `How many shipments have been returned?`

The generated pipeline is displayed alongside results so the query logic is fully auditable.

---

## Data Models

### Shipment
```json
{
  "_id": "SHP_0001",
  "meta": { "sender": "Amazon", "receiver": "Darshan" },
  "outbound": {
    "warehouse_id": "BLR_01",
    "dispatched_at": "2026-05-04T10:00:00",
    "estimated_delivery": "2026-05-06T18:00:00"
  },
  "current_location": { "type": "Point", "coordinates": [77.59, 12.97] },
  "status_logs": [
    { "status": "created", "ts": "2026-05-04T10:00:00" },
    { "status": "in_transit", "ts": "2026-05-04T15:42:03" }
  ],
  "driver_id": "DRV_006",
  "return_info": null
}
```

### Driver
```json
{
  "_id": "DRV_001",
  "name": "Rajesh Kumar",
  "vehicle": "truck",
  "status": "searching",
  "location": { "type": "Point", "coordinates": [77.61, 12.95] }
}
```

---

## Warehouses

| ID | City |
|---|---|
| BLR_01 | Bangalore (Primary) |
| BLR_02 | Bangalore (Secondary) |
| MUM_01 | Mumbai |
| DEL_01 | Delhi |
| HYD_01 | Hyderabad |
