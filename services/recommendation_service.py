# services/recommendation_service.py
import uuid
from fastapi import HTTPException
from database.db import db
from models.recommendations import Recommendation, RecommendationCreate
from pymongo import ReturnDocument

class RecommendationService:
    def __init__(self):
        self.collection = db.get_recommendations_collection()

    async def create_recommendation(self, recommendation: RecommendationCreate) -> Recommendation:
        recommendation_id = str(uuid.uuid4())
        rec_data = recommendation.dict()
        rec_data["id"] = recommendation_id
        self.collection.insert_one(rec_data)
        return Recommendation(**rec_data)

    async def get_all_recommendations(self) -> list[Recommendation]:
        records = self.collection.find()
        return [Recommendation(**rec) for rec in records]

    async def get_recommendation_by_id(self, recommendation_id: str) -> Recommendation:
        record = self.collection.find_one({"id": recommendation_id})
        if not record:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        return Recommendation(**record)

    async def update_recommendation(self, recommendation_id: str, recommendation: RecommendationCreate) -> Recommendation:
        updated = self.collection.find_one_and_update(
            {"id": recommendation_id},
            {"$set": recommendation.dict()},
            return_document=ReturnDocument.AFTER
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        return Recommendation(**updated)

    async def delete_recommendation(self, recommendation_id: str):
        deleted = self.collection.delete_one({"id": recommendation_id})
        if deleted.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        return {"detail": "Recommendation deleted"}
