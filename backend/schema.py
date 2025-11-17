from datetime import date as dt 
from pydantic import BaseModel

class Review(BaseModel):
    id: int | None
    location: str | None
    rating: int | None
    text: str | None
    date : str | dt | None

