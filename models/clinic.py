# models/clinic.py
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class Clinic(BaseModel):
    id: str
    type: str
    name: str
    state: str
    city: str
    specialty: Optional[str] = None
    address: str
    picture_url: Optional[str] = None
    picture_filename: Optional[str] = None
    phone_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email: Optional[str] = None
    location_link: Optional[str] = None
    working_time: Optional[str] = None
    additional_info: Optional[str] = None

class ClinicCreate(BaseModel):
    type: str
    name: str
    state: str
    city: str
    specialty: Optional[str] = None
    address: str
    phone_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email: Optional[str] = None
    location_link: Optional[str] = None
    working_time: Optional[str] = None
    additional_info: Optional[str] = None
