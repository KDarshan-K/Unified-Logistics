from fastapi import APIRouter
from app.services.analytics_service import returns_by_warehouse

router = APIRouter()

@router.get("/analytics/returns")
def get_returns():
    return returns_by_warehouse()