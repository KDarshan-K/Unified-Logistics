from fastapi import APIRouter
from app.services import driver_service

router = APIRouter()

@router.get("/driver/all")
def get_all():
    return driver_service.get_all_drivers()

@router.post("/driver/create")
def create_driver(data: dict):
    return driver_service.create_driver(data)

@router.post("/driver/update-location")
def update_location(data: dict):
    return driver_service.update_driver_location(data)