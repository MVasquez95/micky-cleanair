from fastapi import APIRouter, HTTPException
from app.services.openaq_service import OpenAQService
router = APIRouter()

@router.get("/")
async def get_countries():
    service = OpenAQService()
    try:
        data = await service.get_countries()
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching countries from OpenAQ: {str(e)}"
        )