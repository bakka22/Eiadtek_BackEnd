from pydantic import BaseModel, EmailStr

class ContactInfo(BaseModel):
    email: EmailStr
    phone_number: str
    whatsapp_number: str
