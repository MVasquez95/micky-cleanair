from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.countries import router as countries_router

app = FastAPI(
    title="CleanAir API",
    description="API para consultar y analizar calidad del aire usando datos públicos.",
    version="0.1.0"
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(countries_router, prefix="/countries", tags=["Countries"])