from pydantic import BaseModel

class CitySchema(BaseModel):
    id: int
    country_code: str
    name: str

    class Config:
        orm_mode = True