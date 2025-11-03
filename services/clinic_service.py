# services/clinic_service.py
import uuid
import os
from fastapi import UploadFile, HTTPException, Response
from database.db import db
from models.clinic import Clinic, ClinicCreate
from fastapi.responses import Response
import mimetypes
from pymongo import ReturnDocument
import re

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

class ClinicService:
    def __init__(self):
        self.collection = db.get_clinics_collection()

    async def create_clinic(self, clinic: ClinicCreate, picture: UploadFile | None = None) -> Clinic:
        clinic_id = str(uuid.uuid4())
        picture_filename = None
        picture_url = ""
        safe_name = ""

        if picture != None:
            picture_filename = f"{clinic_id}_{picture.filename}"
            safe_name = sanitize_filename(picture_filename)
            picture_path = os.path.join(UPLOADS_DIR, safe_name)
            with open(picture_path, "wb") as f:
                f.write(picture.file.read())
            picture_url = f"/clinics/picture/{safe_name}"  # relative url

        clinic_data = clinic.dict()
        clinic_data["location_link"] = str(clinic_data["location_link"])
        clinic_data["id"] = clinic_id
        clinic_data["picture_filename"] = safe_name
        clinic_data["picture_url"] = picture_url
        # Insert into DB
        self.collection.insert_one(clinic_data)
        return Clinic(**clinic_data)

    async def get_clinics(self, state: str | None, city: str | None, specialty: str, type: str | None) -> list[Clinic]:
        query = {}
        if state:
            query["state"] = state
        if city:
            query["city"] = city
        if type:
            query["type"] = type
        if specialty:
            query['specialty'] = specialty
        clinics = self.collection.find(query)
        return [Clinic(**clinic) for clinic in clinics]

    async def get_clinic_by_id(self, clinic_id: str) -> Clinic:
        clinic = self.collection.find_one({"id": clinic_id})
        if not clinic:
            raise HTTPException(status_code=404, detail="Clinic not found")
        return Clinic(**clinic)

    async def get_clinic_picture(self, picture_filename: str):
        print("inside clinic service")
        picture_path = os.path.join(UPLOADS_DIR, f"{picture_filename}")
        print(f"picture_path: {picture_path}")
        if not os.path.exists(picture_path):
            raise HTTPException(status_code=404, detail="Picture not found")

        mime_type, _ = mimetypes.guess_type(picture_path)
        mime_type = mime_type or "application/octet-stream"

        with open(picture_path, "rb") as f:
            image_data = f.read()

        return Response(content=image_data, media_type=mime_type)

    async def update_clinic(self, clinic_id: str, clinic: ClinicCreate, picture: UploadFile | None = None) -> Clinic:
        # Prepare updated fields
        update_data = clinic.model_dump()
        update_data["location_link"] = str(update_data["location_link"])

        # Handle picture replacement
        if picture:
            # Optionally remove old picture
            existing = self.collection.find_one({"id": clinic_id})
            if existing and existing.get("picture_filename"):
                old_path = os.path.join(UPLOADS_DIR, existing["picture_filename"])
                try:
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass
            new_filename = f"{clinic_id}_{picture.filename}"
            picture_path = os.path.join(UPLOADS_DIR, new_filename)
            with open(picture_path, "wb") as f:
                f.write(picture.file.read())
            update_data["picture_filename"] = new_filename
            update_data["picture_url"] = f"/clinics/picture/{new_filename}"
        # Apply update
        updated = self.collection.find_one_and_update(
            {"id": clinic_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Clinic not found")
        return Clinic(**updated)

    async def delete_clinic(self, clinic_id: str):
        clinic = self.collection.find_one({"id": clinic_id})
        if not clinic:
            raise HTTPException(status_code=404, detail="Clinic not found")
        # remove picture file if exists
        if clinic.get("picture_filename"):
            path = os.path.join(UPLOADS_DIR, clinic["picture_filename"])
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        result = self.collection.delete_one({"id": clinic_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete clinic")
        return {"detail": "Clinic deleted"}
