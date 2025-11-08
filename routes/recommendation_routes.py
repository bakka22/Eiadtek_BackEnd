# routes/recommendation_routes.py
from fastapi import APIRouter, Depends
from typing import List
from models.recommendations import Recommendation, RecommendationCreate
from services.recommendation_service import RecommendationService
from utils.security import get_current_user, require_role

router = APIRouter()
recommendation_service = RecommendationService()

@router.post("/", response_model=Recommendation)
async def create_recommendation(
    recommendation: Recommendation,
    current_user: dict = Depends(get_current_user),
):
    return await recommendation_service.create_recommendation(recommendation)

@router.get("/", response_model=List[Recommendation])
async def get_all_recommendations(
    current_user: dict = Depends(get_current_user)
):
    return await recommendation_service.get_all_recommendations()

@router.get("/{id}", response_model=Recommendation)
async def get_recommendation_by_id(
    id: str,
    current_user: dict = Depends(get_current_user)
):
    return await recommendation_service.get_recommendation_by_id(id)


@router.delete("/{id}")
async def delete_recommendation(
    id: str,
    current_user: dict = Depends(get_current_user),
    _ = Depends(require_role("owner"))
):
    return await recommendation_service.delete_recommendation(id)
