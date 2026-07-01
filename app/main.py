from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import shipment_routes, driver_routes, analytics_routes
from app.services.analytics_service import returns_by_warehouse
from app.services.shipment_service import get_all_shipments, get_shipment
from app.services.driver_service import get_all_drivers
from app.routes import shipment_routes, driver_routes, analytics_routes, query_routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(shipment_routes.router)
app.include_router(driver_routes.router)
app.include_router(analytics_routes.router)
app.include_router(query_routes.router)
@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "shipments": get_all_shipments(),
        "drivers": get_all_drivers(),
        "returns": returns_by_warehouse(),
    })

@app.get("/shipments")
def shipments_page(request: Request):
    return templates.TemplateResponse("shipments.html", {
        "request": request,
        "shipments": get_all_shipments(),
    })

@app.get("/shipments/{shipment_id}")
def shipment_detail(request: Request, shipment_id: str):
    return templates.TemplateResponse("shipments.html", {
        "request": request,
        "shipment": get_shipment(shipment_id),
    })

@app.get("/drivers")
def drivers_page(request: Request):
    return templates.TemplateResponse("drivers.html", {
        "request": request,
        "drivers": get_all_drivers(),
    })