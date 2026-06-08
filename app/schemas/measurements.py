from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MeasurementSchema(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    parameter: Optional[str] = None
    value: float
    unit: Optional[str] = None
    measured_at: Optional[datetime] = None
    source_name: Optional[str] = None
    
    class Config:
        orm_mode = True