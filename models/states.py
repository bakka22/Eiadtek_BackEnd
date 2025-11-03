from pydantic import BaseModel
from typing import List

class City(BaseModel):
    en: str
    ar: str

class State(BaseModel):
    en: str
    ar: str
    cities: List[City]

class StateCreate(BaseModel):
    en: str
    ar: str
    cities: List[City]
