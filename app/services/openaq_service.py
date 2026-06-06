import httpx
from app.core.config import settings

class OpenAQService:
    def __init__(self):
        self.base_URL = settings.OPENAQ_BASE_URL
        self.headers = {
            "X-API-Key": settings.OPENAQ_API_KEY
        }
    async def get_countries(self):
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_URL}/countries", headers=self.headers)
            response.raise_for_status()
            return response.json()
        
    async def get_cities(self, country_code: str):
        params = {}
        if country_code:
            params["country"] = country_code

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_URL}/cities", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        
    async def get_latest_measurements(self, city: str = None, parameter: str = None):
        params = {}
        if city:
            params["city"] = city
        if parameter:
            params["parameter"] = parameter
        
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_URL}/measurements/latest", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        