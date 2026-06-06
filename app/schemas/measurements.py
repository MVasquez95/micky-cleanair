from pydantic import BaseModel
from datetime import datetime

class MeasurementSchema(BaseModel):
    country: str
    city: str
    location: str
    parameter: str
    value: float
    unit: str
    measured_at: datetime
    source_name: str | None = None

    class Config:
        orm_mode = True