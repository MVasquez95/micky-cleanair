from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.openaq_service import OpenAQService
from app.schemas.locations import LocationSchema

router = APIRouter()

@router.get("/", response_model=List[LocationSchema])
async def get_locations(country_code: Optional[str] = Query(None, description="Filter by ISO country code")):
    """Obtiene las locations de OpenAQ, filtradas por país opcionalmente.
    
    Args:
        country_code (str, optional): Código ISO del país para filtrar locations. Defaults to None.

    Returns:
        List[LocationSchema]: Lista de locations con id, país y nombre de ciudad.
    
    Raises:
        HTTPException: Si ocurre un error al llamar a OpenAQ
    """
    service = OpenAQService()
    try:
        data = await service.get_locations(country_code)
        locations = []
        for loc in data.get("results", []):
            city_name = loc.get("city") or loc.get("name") or "Unknown"
            if isinstance(city_name, (list, dict)):
                city_name = str(city_name)
            locations.append({
                "id": loc.get("id"),
                "country_code": str(loc.get("country", {}).get("code", "Unknown")),
                "name": city_name})
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations: {str(e)}")