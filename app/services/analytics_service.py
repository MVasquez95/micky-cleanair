from typing import List, Dict
from app.repositories.measurement_repository import MeasurementRepository

class AnalyticsService:
    """Servicio para cálculos agregados de contaminación."""

    def __init__(self, repo: MeasurementRepository):
        """
        Inicializa el AnalyticsService con un repositorio de measurements.
        
        Args:
            repo (MeasurementRepository): Instancia del repository para acceder a la DB.
        """
        self.repo = repo

    def average_by_parameter(self, location_id: str, parameter: str) -> Dict:
        """
        Devuelve el promedio, máximo y mínimo de un parámetro para un location específico.

        Args:
            location_id (str): ID del location.
            parameter (str): Nombre del parámetro, ej: 'pm25'.

        Returns:
            Dict: {"parameter": parameter, "avg": float, "max": float, "min": float}
        """
        return self.repo.get_average_by_parameter(location_id, parameter)

    def top_locations_by_parameter(self, parameter: str, top_n: int = 10) -> List[Dict]:
        """
        Devuelve los top N locations con mayor promedio de un parámetro.

        Args:
            parameter (str): Nombre del parámetro.
            top_n (int, optional): Número de locations a devolver. Defaults to 10.

        Returns:
            List[Dict]: [{"location": str, "avg_value": float}, ...]
        """
        return self.repo.get_top_locations_by_parameter(parameter, top_n)