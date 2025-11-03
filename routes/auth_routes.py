from fastapi import APIRouter, Depends, HTTPException, status
from utils.forms import OAuth2EmailRequestForm
from models.user import UserCreate, Token
from services.auth_service import AuthService
from datetime import timedelta

router = APIRouter()
auth_service = AuthService()

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    return await auth_service.register_user(user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2EmailRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}