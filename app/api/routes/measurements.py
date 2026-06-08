from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from dateutil.parser import parse
from app.services.openaq_service import OpenAQService
from app.schemas.measurements import MeasurementSchema

router = APIRouter()

@router.get("/{location_id}/latest", response_model=List[MeasurementSchema])
async def get_latest_measurements(
    location_id: int = Path(..., description="ID del location"),
    parameter: Optional[str] = Query(None, description="Filter by pollutant parameter, e.g., pm25, o3"),
    only_latest: Optional[bool] = Query(False, description="Return only the latest measurement per parameter")
):
    """
    Obtiene las mediciones de un location a través de sus sensores, filtrando opcionalmente por parámetro y/o devolviendo solo la más reciente.
    
    Args:
        location_id (int): ID del location.
        parameter (str, optional): Parámetro de contaminante para filtrar.
        only_latest (bool, optional): Si True, devuelve solo la medición más reciente por parameter.
    
    Returns:
        List[MeasurementSchema]: Lista de mediciones con los datos solicitados.

    Raises:
        HTTPException: Si ocurre un error al llamar a OpenAQ.
    """
    service = OpenAQService()
    try:
        sensors_data = await service.get_sensors_by_location(location_id)
        measurements = []

        for sensor in sensors_data.get("results", []):
            sensor_id = sensor.get("id")
            if not sensor_id:
                continue

            sensor_measurements = await service.get_measurements_by_sensor(sensor_id)

            for m in sensor_measurements.get("results", []):
                param_obj = m.get("parameter") if isinstance(m.get("parameter"), dict) else {"name": m.get("parameter"), "units": m.get("unit")}
                param_name = param_obj.get("name")
                param_unit = param_obj.get("units")

                # Filtrar por parámetro si se especifica
                if parameter and param_name != parameter:
                    continue

                measured_at_raw = m.get("datetime")
                try:
                    measured_at = parse(measured_at_raw) if measured_at_raw else None
                except Exception:
                    measured_at = None

                measurements.append({
                    "country": None,
                    "city": None,
                    "location": None,
                    "parameter": param_name,
                    "value": m.get("value") or 0,
                    "unit": param_unit,
                    "measured_at": measured_at,
                    "source_name": sensor.get("sourceName")
                })

        if only_latest:
            latest_per_param = {}
            for meas in measurements:
                param = meas["parameter"]
                current = latest_per_param.get(param)
                if not current or (meas["measured_at"] and meas["measured_at"] > current["measured_at"]):
                    latest_per_param[param] = meas
            measurements = list(latest_per_param.values())

        return measurements

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching measurements for location {location_id}: {str(e)}"
        )