# services/auth_service.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from database.db import db
from models.user import UserCreate, UserInDB
from utils.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.collection = db.get_users_collection()

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def register_user(self, user: UserCreate):
        if self.collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = self.get_password_hash(user.password)
        user_data = {
            "email": user.email,
            "hashed_password": hashed_password,
            "role": user.role
        }
        self.collection.insert_one(user_data)
        return {"email": user.email, "role": user.role}

    async def authenticate_user(self, email: str, password: str):
        user = self.collection.find_one({"email": email})
        if not user:
            return False
        if not self.verify_password(password, user["hashed_password"]):
            return False
        # Return a clean UserInDB without Mongo's _id (pydantic will expect fields)
        return UserInDB(email=user["email"], role=user["role"], hashed_password=user["hashed_password"])

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        to_encode.update({"sub": data.get("sub")})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
