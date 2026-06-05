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