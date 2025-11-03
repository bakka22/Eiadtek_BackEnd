# routes/clinic_routes.py
from fastapi import APIRouter, UploadFile, File, Depends, Form, Query, Header
from models.clinic import Clinic, ClinicCreate
from services.clinic_service import ClinicService
from typing import List, Optional
from utils.security import get_current_user, require_role
import json
from urllib.parse import unquote
import logging

router = APIRouter()
clinic_service = ClinicService()

@router.post("/", response_model=Clinic)
async def create_clinic(
    clinic: str = Form(...),
    picture: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),  # Require auth
    _ = Depends(require_role("owner"))  # Require owner role
):
    """
    Expect a multipart/form-data request with:
      - "clinic": JSON string matching ClinicCreate
      - "picture": optional file
    """
    clinic_data = json.loads(clinic)
    clinic_obj = ClinicCreate(**clinic_data)
    return await clinic_service.create_clinic(clinic_obj, picture)

@router.get("/", response_model=List[Clinic])
async def get_clinics(
    state: str|None = Header(None, alias="X-State"),
    city: str|None = Header(None, alias="X-City"),
    specialty: str|None = Header(None, alias="X-Specialty"),
    type: str|None = Header(None, alias="X-type"),
    current_user: dict = Depends(get_current_user)
):
    """
    Use query parameters: /clinics?state=...&city=...&specialty=...
    """
    return await clinic_service.get_clinics(state, city, specialty, type)

@router.get("/{id}", response_model=Clinic)
async def get_clinic_by_id(id: str, current_user: dict = Depends(get_current_user)):
    return await clinic_service.get_clinic_by_id(id)

@router.get("/picture/{picture_filename}")
async def get_clinic_picture(picture_filename: str):
    """
    Returns the uploaded clinic picture by filename.
    Example: GET /clinics/picture/1234abcd_myclinic.png
    """
    decoded_filename = unquote(picture_filename)
    print(decoded_filename, flush=True)
    return await clinic_service.get_clinic_picture(decoded_filename)

@router.put("/{id}", response_model=Clinic)
async def update_clinic(
    id: str,
    clinic: str = Form(...),
    picture: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    clinic_data = json.loads(clinic)
    clinic_obj = ClinicCreate(**clinic_data)
    return await clinic_service.update_clinic(id, clinic_obj, picture)

@router.delete("/{id}")
async def delete_clinic(
    id: str,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await clinic_service.delete_clinic(id)
