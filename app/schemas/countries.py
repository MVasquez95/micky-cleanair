from pydantic import BaseModel

class CountrySchema(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True