from fastapi import APIRouter, Query
from app.services.analytics_service import AnalyticsService
from app.repositories.measurement_repository import MeasurementRepository
from app.db.database import SessionLocal

router = APIRouter()

db = SessionLocal()
repo = MeasurementRepository(db)
service = AnalyticsService(repo)

@router.get("/average")
def average_parameter(
    location_id: str = Query(..., description="ID del location"),
    parameter: str = Query(..., description="Nombre del parámetro, ej: 'pm25'")
):
    """Promedio, máximo y mínimo de un parámetro para un location."""
    return service.average_by_parameter(location_id, parameter)

@router.get("/top")
def top_locations(
    parameter: str = Query(..., description="Nombre del parámetro, ej: 'pm25'"),
    top_n: int = Query(10, description="Número de locations a devolver")
):
    """Top N locations con mayor promedio de un parámetro."""
    return service.top_locations_by_parameter(parameter, top_n)