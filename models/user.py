from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    role: str  # "customer" or "owner"

class UserCreate(BaseModel):
    password: str
    email: EmailStr
    role: str  # "customer" or "owner"

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str