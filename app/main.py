from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.countries import router as countries_router
from app.api.routes.locations import router as locations_router
from app.api.routes.measurements import router as measurements_router

app = FastAPI(
    title="CleanAir API",
    description="API para consultar y analizar calidad del aire usando datos públicos.",
    version="0.1.0"
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(countries_router, prefix="/countries", tags=["Countries"])
app.include_router(locations_router, prefix="/locations", tags=["Locations"])
app.include_router(measurements_router, prefix="/measurements", tags=["Measurements"])