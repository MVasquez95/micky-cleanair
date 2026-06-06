from fastapi import APIRouter, HTTPException
from typing import List
from app.services.openaq_service import OpenAQService
from app.schemas.cities import CitySchema

router = APIRouter()

@router.get("/", response_model=List[CitySchema])
async def get_cities(country_code: str = None):
    service = OpenAQService()
    try:
        data = await service.get_cities(country_code)
        cities = [{"id": c["id"], "country_code": c["country"], "name": c["name"]}
                  for c in data["results"]]
        return cities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cities: {str(e)}")