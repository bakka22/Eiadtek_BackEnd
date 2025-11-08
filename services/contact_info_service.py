# services/contact_info_service.py
import uuid
from fastapi import HTTPException
from database.db import db
from models.contact_info import ContactInfo
from pymongo import ReturnDocument

class ContactInfoService:
    def __init__(self):
        self.collection = db.get_contact_infos_collection()

    async def create_contact_info(self, contact_info: ContactInfo) -> ContactInfo:
        contact_id = str(uuid.uuid4())
        contact_data = contact_info.dict()
        contact_data["id"] = contact_id
        self.collection.insert_one(contact_data)
        return ContactInfo(**contact_data)

    async def get_all_contact_infos(self) -> list[ContactInfo]:
        records = self.collection.find()
        return [ContactInfo(**rec) for rec in records]

    async def get_contact_info_by_id(self, contact_id: str) -> ContactInfo:
        record = self.collection.find_one({"id": contact_id})
        if not record:
            raise HTTPException(status_code=404, detail="Contact info not found")
        return ContactInfo(**record)

    async def update_contact_info(self, contact_id: str, contact_info: ContactInfo) -> ContactInfo:
        updated = self.collection.find_one_and_update(
            {"id": contact_id},
            {"$set": contact_info.dict()},
            return_document=ReturnDocument.AFTER
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Contact info not found")
        return ContactInfo(**updated)

    async def delete_contact_info(self, contact_id: str):
        deleted = self.collection.delete_one({"id": contact_id})
        if deleted.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Contact info not found")
        return {"detail": "Contact info deleted"}
