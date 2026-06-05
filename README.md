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
DATABASE_URL=postgresql://user:password@localhost:5432/cleanair_db  
OPENAQ_API_KEY=tu_api_key_aqui  
OPENAQ_BASE_URL=https://api.openaq.org/v3

## Levantar proyecto

```bash
# Levantar PostgreSQL
docker compose up -d

# Activar venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear tablas iniciales
python -m scripts.create_tables

# Levantar FastAPI
uvicorn app.main:app --reload
