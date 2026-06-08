from fastapi import APIRouter, HTTPException
from typing import List
from app.services.openaq_service import OpenAQService
from app.schemas.countries import CountrySchema

router = APIRouter()

@router.get("/", response_model=List[CountrySchema])
async def get_countries():
    """Obtiene la lista de países disponibles en OpenAQ.

    Returns:
        List[CountrySchema]: Lista de países disponibles.

    Raises:
        HTTPException: Si ocurre un error al llamar a OpenAQ
    """
    service = OpenAQService()
    try:
        data = await service.get_countries()
        #Normalización de datos para que coincidan con el esquema CountrySchema
        countries = [{"id": c["id"], "code": c["code"], "name": c["name"]}
        for c in data["results"]]
        return countries
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching countries from OpenAQ: {str(e)}"
        )