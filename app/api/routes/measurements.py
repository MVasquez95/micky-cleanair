from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.openaq_service import OpenAQService
from app.schemas.measurements import MeasurementSchema

router = APIRouter()

@router.get("/latest", response_model=List[MeasurementSchema])
async def get_latest_measurements(city: str = Query(None), parameter: str = Query(None)):
    service = OpenAQService()
    try:
        data = await service.get_latest_measurements(city, parameter)
        measurements = []
        for m in data["results"]:
            for p in m["parameters"]:
                measurements.append({
                    "country": m["country"],
                    "city": m["city"],
                    "location": m["location"],
                    "parameter": p["parameter"],
                    "value": p["value"],
                    "unit": p["unit"],
                    "measured_at": p["lastUpdated"],
                    "source_name": m.get("sourceName")
                })
        return measurements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest measurements: {str(e)}")