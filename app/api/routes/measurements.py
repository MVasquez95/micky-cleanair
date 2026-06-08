from fastapi import APIRouter, HTTPException, Path
from typing import List
from dateutil.parser import parse
from app.services.openaq_service import OpenAQService
from app.schemas.measurements import MeasurementSchema

router = APIRouter()

@router.get("/{location_id}/latest", response_model=List[MeasurementSchema])
async def get_latest_measurements(location_id: int = Path(..., description="ID del location")):
    """Obtiene las mediciones más recientes de un location específico.

    Args:
        location_id (int): ID del location para obtener mediciones.

    Returns:
        List[MeasurementSchema]: Lista de mediciones más recientes.

    Raises:
        HTTPException: Si ocurre un error al llamar a OpenAQ
    """
    service = OpenAQService()
    try:
        # 1️⃣ Obtener sensores del location
        sensors_data = await service.get_sensors_by_location(location_id)
        measurements = []

        for sensor in sensors_data.get("results", []):
            sensor_id = sensor.get("id")
            if not sensor_id:
                continue

            # 2️⃣ Obtener mediciones reales del sensor
            sensor_measurements = await service.get_measurements_by_sensor(sensor_id)

            for m in sensor_measurements.get("results", []):
                param = m.get("parameter", {})
                measured_at_raw = m.get("datetime")
                try:
                    measured_at = parse(measured_at_raw) if measured_at_raw else None
                except Exception:
                    measured_at = None

                measurements.append({
                    "country": sensor.get("country"),
                    "city": sensor.get("city") or sensor.get("location"),
                    "location": sensor.get("location"),
                    "parameter": param.get("name") if isinstance(param, dict) else param,
                    "value": m.get("value") or 0,
                    "unit": param.get("units") if isinstance(param, dict) else None,
                    "measured_at": measured_at,
                    "source_name": sensor.get("sourceName")
                })

        return measurements
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching measurements for location {location_id}: {str(e)}"
        )