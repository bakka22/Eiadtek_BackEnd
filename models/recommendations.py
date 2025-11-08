from pydantic import BaseModel

class Recommendation(BaseModel):
    content: str
