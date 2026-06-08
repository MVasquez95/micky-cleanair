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
    
    async def get_measurements_with_location(self, location_id: int):
        """Devuelve las mediciones de un location junto con datos de country, city y location."""
        
        async with httpx.AsyncClient(timeout=15) as client:
            loc_resp = await client.get(f"{self.base_url}/locations/{location_id}", headers=self.headers)
            loc_resp.raise_for_status()
            loc_data = loc_resp.json()["results"][0]

        sensors_resp = await client.get(f"{self.base_url}/locations/{location_id}/sensors", headers=self.headers)
        sensors_resp.raise_for_status()
        sensors_data = sensors_resp.json().get("results", [])

        measurements = []

        for sensor in sensors_data:
            sensor_id = sensor.get("id")
            if not sensor_id:
                continue

            meas_resp = await client.get(f"{self.base_url}/sensors/{sensor_id}/measurements", headers=self.headers)
            meas_resp.raise_for_status()
            for m in meas_resp.json().get("results", []):
                param_obj = m.get("parameter") if isinstance(m.get("parameter"), dict) else {"name": m.get("parameter"), "units": m.get("unit")}
                param_name = param_obj.get("name")
                param_unit = param_obj.get("units")

                measurements.append({
                    "country": loc_data.get("country"),
                    "city": loc_data.get("city"),
                    "location": loc_data.get("name"),
                    "parameter": param_name,
                    "unit": param_unit,
                    "value": m.get("value") or 0,
                    "measured_at": m.get("datetime"),
                    "source_name": sensor.get("sourceName")
                })

        return measurements