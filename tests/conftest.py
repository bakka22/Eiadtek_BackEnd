import pytest
import pymongo
from fastapi.testclient import TestClient
from main import app
from database.db import Database
from passlib.context import CryptContext

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = Database()
    yield db
    # Cleanup: Drop collections after tests
    db.get_clinics_collection().drop()
    db.get_users_collection().drop()

@pytest.fixture(scope="module")
def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(scope="module")
def test_users(db, pwd_context):
    users_collection = db.get_users_collection()
    users_collection.delete_many({})
    users = [
        {
            "username": "owner",
            "hashed_password": pwd_context.hash("ownerpass"),
            "role": "owner"
        },
        {
            "username": "customer",
            "hashed_password": pwd_context.hash("customerpass"),
            "role": "customer"
        }
    ]
    users_collection.insert_many(users)
    return users