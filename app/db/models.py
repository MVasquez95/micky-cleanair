from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country: Mapped[str] = mapped_column(String(10), index=True)
    city: Mapped[str] = mapped_column(String(120), index=True)
    location: Mapped[str] = mapped_column(String(200), index=True)
    parameter: Mapped[str] = mapped_column(String(50), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(30))
    measured_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    source_name: Mapped[str | None] = mapped_column(String(120), nullable=True)