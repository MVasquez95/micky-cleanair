from pydantic import BaseModel

class LocationSchema(BaseModel):
    id: int
    country_code: str
    name: str

    class Config:
        orm_mode = True