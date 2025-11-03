# routes/state_routes.py
from fastapi import APIRouter, Depends
from models.states import State, StateCreate, City
from services.states_service import StateService
from typing import List
from utils.security import get_current_user, require_role

router = APIRouter()
state_service = StateService()

@router.post("/", response_model=State)
async def create_state(
    state: StateCreate,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))  # Only admin can add new states
):
    return await state_service.create_state(state)

@router.get("/", response_model=List[State])
async def get_states(current_user: dict = Depends(get_current_user)):
    return await state_service.get_states()

@router.get("/{en}", response_model=State)
async def get_state_by_name(en: str, current_user: dict = Depends(get_current_user)):
    return await state_service.get_state_by_name(en)

@router.put("/{en}", response_model=State)
async def update_state(
    en: str,
    state: StateCreate,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await state_service.update_state(en, state)

@router.post("/{en}/cities", response_model=State)
async def add_city(
    en: str,
    city: City,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await state_service.add_city(en, city)

@router.delete("/{en}/cities/{city_en}")
async def remove_city(
    en: str,
    city_en: str,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await state_service.remove_city(en, city_en)

@router.delete("/{en}")
async def delete_state(
    en: str,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await state_service.delete_state(en)
