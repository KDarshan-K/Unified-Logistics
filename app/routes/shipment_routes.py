from fastapi import APIRouter, Request
from app.services import shipment_service

router = APIRouter()

@router.get("/shipment/all")
def get_all():
    return shipment_service.get_all_shipments()

@router.post("/shipment/create")
def create(data: dict):
    return shipment_service.create_shipment(data)

@router.post("/shipment/update")
def update(data: dict):
    return shipment_service.update_shipment_location(data)

@router.get("/shipment/{shipment_id}/status-fragment")
def status_fragment(shipment_id: str, request: Request):
    from app.main import templates
    shipment = shipment_service.get_shipment(shipment_id)
    return templates.TemplateResponse("_status_fragment.html", {
        "request": request,
        "shipment": shipment,
    })

@router.get("/shipment/{shipment_id}")
def get(shipment_id: str):
    return shipment_service.get_shipment(shipment_id)

@router.post("/shipment/assign-driver")
def assign(data: dict):
    return shipment_service.assign_driver(data["shipment_id"])

@router.post("/shipment/return")
def return_shipment(data: dict):
    return shipment_service.initiate_return(data)