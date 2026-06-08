# Micky-CleanAir

API backend avanzada con **FastAPI** para consultar y analizar calidad del aire usando datos de **OpenAQ**.  
El proyecto incluye:

- FastAPI con endpoints asíncronos
- PostgreSQL levantado en Docker
- Pydantic schemas para validación de datos
- Estructura profesional por capas: routers, services, repositories
- Scripts de mantenimiento (`scripts/`)
- README, .gitignore y MIT License

## Requisitos

- Python 3.11+
- Docker Desktop
- pipenv o virtualenv (opcional)

## Variables de entorno

Crea un archivo `.env` con:  
# example.env
DATABASE_URL=postgresql+psycopg2://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5432/<POSTGRES_DB>  
OPENAQ_API_KEY=your_openaq_api_key_here  
OPENAQ_BASE_URL=https://api.openaq.org/v3  

## Levantar proyecto

```bash
# Levantar PostgreSQL en Docker
docker compose up -d

# Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear tablas iniciales
python -m scripts.create_tables

# Levantar FastAPI
uvicorn app.main:app --reload
```

## Endpoint: /countries/

Devuelve la lista de países disponibles en OpenAQ, normalizada con Pydantic schema `CountrySchema`.  

### Request
GET /countries/

### Response (ejemplo)

```json
[
  { "id": 1, "code": "ID", "name": "Indonesia" },
  { "id": 2, "code": "PE", "name": "Peru" }
]
```

## Endpoint: /locations/
Devuelve las locations disponibles. Se puede filtrar por país (ISO).

### Request
GET /locations/?country_code=PE

```json
[
  { "id": 819, "country_code": "PE", "name": "Ate" },
  { "id": 2277, "country_code": "PE", "name": "CARABAYLLO" }
]
```

## Endpoint: /measurements/{location_id}/latest
Devuelve las mediciones de un location, opcionalmente filtradas por parámetro.

### Request
GET /measurements/1461/latest?parameter=pm25&only_latest=true

```json
[
  {
    "country": "PE",
    "city": "Lima",
    "location": "Lima",
    "parameter": "pm25",
    "unit": "µg/m³",
    "value": 12.5,
    "measured_at": "2026-06-08T03:37:31.512Z",
    "source_name": "AirNow"
  }
]
```

## /analytics/average
Devuelve promedio, máximo y mínimo de un parámetro para un location específico.

### Request
GET /analytics/average?location_id=819&parameter=pm25

```json
{
  "parameter": "pm25",
  "avg": 35.2,
  "max": 85,
  "min": 12
}
```

## /analytics/top
Devuelve los top N locations con mayor promedio de un parámetro.

### Request
GET /analytics/top?parameter=pm25&top_n=5

```json
[
  { "location": "Ate", "avg_value": 85 },
  { "location": "CARABAYLLO", "avg_value": 78 }
]
```

## Notas finales

- La API es asíncrona, modular y preparada para ser consumida por un frontend o dashboards.
- La base de datos PostgreSQL permite persistir measurements y hacer analítica posterior sin afectar la consulta live a OpenAQ.
- Se incluye `MeasurementRepository` y `AnalyticsService` para separar acceso a DB y lógica de negocio, demostrando arquitectura limpia.