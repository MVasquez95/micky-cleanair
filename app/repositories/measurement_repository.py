from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Measurement
from typing import List, Dict

class MeasurementRepository:
    """Repositorio para la tabla measurements."""

    def __init__(self, db: Session):
        self.db = db

    def add_measurements(self, measurements: List[dict]):
        """Inserta múltiples mediciones en la tabla."""
        for m in measurements:
            obj = Measurement(
                country=m.get("country"),
                city=m.get("city"),
                location=m.get("location"),
                parameter=m.get("parameter"),
                value=m.get("value", 0),
                unit=m.get("unit"),
                measured_at=m.get("measured_at"),
                source_name=m.get("source_name")
            )
            self.db.add(obj)
        self.db.commit()

    def get_by_location(self, location_id: str) -> List[Measurement]:
        """Obtiene todas las mediciones de un location específico."""
        return self.db.query(Measurement).filter(Measurement.location==location_id).all()

    def get_average_by_parameter(self, location_id: str, parameter: str) -> Dict:
        """Calcula promedio, máximo y mínimo de un parámetro en un location."""
        result = self.db.query(
            func.avg(Measurement.value).label("avg_value"),
            func.max(Measurement.value).label("max_value"),
            func.min(Measurement.value).label("min_value")
        ).filter(
            Measurement.location==location_id,
            Measurement.parameter==parameter
        ).first()
        return {
            "parameter": parameter,
            "avg": result.avg_value if result else None,
            "max": result.max_value if result else None,
            "min": result.min_value if result else None
        }

    def get_top_locations_by_parameter(self, parameter: str, top_n: int = 10) -> List[Dict]:
        """Devuelve los top N locations con mayor promedio de un parámetro."""
        results = self.db.query(
            Measurement.location,
            func.avg(Measurement.value).label("avg_value")
        ).filter(
            Measurement.parameter==parameter
        ).group_by(
            Measurement.location
        ).order_by(
            func.avg(Measurement.value).desc()
        ).limit(top_n).all()
        return [{"location": r.location, "avg_value": r.avg_value} for r in results]