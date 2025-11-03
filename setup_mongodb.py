import pymongo
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["clinic_db"]
clinics_collection = db["clinics"]
users_collection = db["users"]

# Create indexes
clinics_collection.create_index([("state", pymongo.ASCENDING), ("city", pymongo.ASCENDING)])
users_collection.create_index("username", unique=True)
print("Indexes created successfully.")

# Insert sample clinic
sample_clinic = {
    "id": str(uuid.uuid4()),
    "name": "Sample Clinic",
    "state": "Khartoum",
    "city": "Omdurman",
    "address": "123 Main Street",
    "picture_url": "http://your-server.com/uploads/sample.jpg",
    "phone_numbers": ["+249123456789", "+249987654321"],
    "email": "contact@sampleclinic.com",
    "location_link": "https://maps.google.com/?q=15.5881,32.5666"
}
clinics_collection.insert_one(sample_clinic)
print("Sample clinic inserted.")

# Insert sample users
sample_owner = {
    "username": "owner",
    "hashed_password": pwd_context.hash("ownerpass"),
    "role": "owner"
}
sample_customer = {
    "username": "customer",
    "hashed_password": pwd_context.hash("customerpass"),
    "role": "customer"
}
users_collection.insert_many([sample_owner, sample_customer])
print("Sample users inserted: owner/ownerpass (owner), customer/customerpass (customer)")