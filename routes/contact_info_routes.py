# routes/contact_info_routes.py
from fastapi import APIRouter, Depends
from typing import List
from models.contact_info import ContactInfo
from services.contact_info_service import ContactInfoService
from utils.security import get_current_user, require_role

router = APIRouter()
contact_service = ContactInfoService()

@router.post("/", response_model=ContactInfo)
async def create_contact_info(
    contact_info: ContactInfo,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await contact_service.create_contact_info(contact_info)

@router.get("/", response_model=List[ContactInfo])
async def get_all_contact_infos(
    current_user: dict = Depends(get_current_user)
):
    return await contact_service.get_all_contact_infos()

@router.get("/{id}", response_model=ContactInfo)
async def get_contact_info_by_id(
    id: str,
    current_user: dict = Depends(get_current_user)
):
    return await contact_service.get_contact_info_by_id(id)

@router.put("/{id}", response_model=ContactInfo)
async def update_contact_info(
    id: str,
    contact_info: ContactInfo,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await contact_service.update_contact_info(id, contact_info)

@router.delete("/{id}")
async def delete_contact_info(
    id: str,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await contact_service.delete_contact_info(id)
