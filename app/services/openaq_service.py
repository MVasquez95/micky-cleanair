import httpx
from app.core.config import settings

class OpenAQService:
    """Service class para interactuar con la API OpenAQ v3."""

    def __init__(self):
        """Inicializa el service con base_url y headers."""
        self.base_url = settings.OPENAQ_BASE_URL
        self.headers = {"X-API-Key": settings.OPENAQ_API_KEY}

    async def get_countries(self) -> dict:
        """Obtiene la lista de países desde OpenAQ."""
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/countries", headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_locations(self, country_code: str = None) -> dict:
        """Obtiene locations desde OpenAQ v3, filtrando opcionalmente por país."""
        params = {"limit": 1000}
        if country_code:
            params["iso"] = country_code

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/locations", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def get_sensors_by_location(self, location_id: int) -> dict:
        """Obtiene los sensores asociados a un location."""
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/locations/{location_id}/sensors", headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_measurements_by_sensor(self, sensor_id: int, limit: int = 100) -> dict:
        """Obtiene mediciones crudas de un sensor específico."""
        params = {"limit": limit}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/sensors/{sensor_id}/measurements", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()