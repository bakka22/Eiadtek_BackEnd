# services/state_service.py
from fastapi import HTTPException
from database.db import db
from models.states import State, StateCreate, City
from pymongo import ReturnDocument
import uuid

class StateService:
    def __init__(self):
        self.collection = db.get_states_collection()

    async def create_state(self, state: StateCreate) -> State:
        # Check if state already exists (match by English name)
        existing = self.collection.find_one({"en": state.en})
        if existing:
            raise HTTPException(status_code=400, detail="State already exists")

        state_id = str(uuid.uuid4())
        state_data = state.model_dump()
        state_data["id"] = state_id

        self.collection.insert_one(state_data)
        return State(**state_data)

    async def get_states(self) -> list[State]:
        states = self.collection.find()
        return [State(**state) for state in states]

    async def get_state_by_name(self, en: str) -> State:
        state = self.collection.find_one({"en": en})
        if not state:
            raise HTTPException(status_code=404, detail="State not found")
        return State(**state)

    async def update_state(self, en: str, state: StateCreate) -> State:
        updated = self.collection.find_one_and_update(
            {"en": en},
            {"$set": state.model_dump()},
            return_document=ReturnDocument.AFTER
        )
        if not updated:
            raise HTTPException(status_code=404, detail="State not found")
        return State(**updated)

    async def add_city(self, state_en: str, city: City):
        city_dict = city.model_dump()
        updated = self.collection.find_one_and_update(
            {"en": state_en},
            {"$addToSet": {"cities": city_dict}},  # avoids duplicates
            return_document=ReturnDocument.AFTER
        )
        if not updated:
            raise HTTPException(status_code=404, detail="State not found")
        return State(**updated)

    async def remove_city(self, state_en: str, city_en: str):
        updated = self.collection.find_one_and_update(
            {"en": state_en},
            {"$pull": {"cities": {"en": city_en}}},
            return_document=ReturnDocument.AFTER
        )
        if not updated:
            raise HTTPException(status_code=404, detail="State not found")
        return {"detail": f"City '{city_en}' removed from {state_en}", "state": updated}

    async def delete_state(self, en: str):
        result = self.collection.delete_one({"en": en})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="State not found")
        return {"detail": "State deleted successfully"}
