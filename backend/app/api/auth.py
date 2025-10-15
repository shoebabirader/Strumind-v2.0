"""
Authentication endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.security import (
    create_access_token, get_password_hash, verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES, Token, get_current_active_user, TokenData
)
from app.core.legal import get_engineering_disclaimer, create_acceptance_record, EngineeringDisclaimer

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    license_number: Optional[str] = None
    organization: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    accepted_disclaimer: bool


class DisclaimerAcceptance(BaseModel):
    accepted: bool


# Mock user database (replace with real database in production)
fake_users_db = {
    "demo": {
        "id": 1,
        "username": "demo",
        "email": "demo@strumind.com",
        "full_name": "Demo User",
        "hashed_password": get_password_hash("demo123"),
        "is_active": True,
        "accepted_disclaimer": True
    }
}


@router.get("/disclaimer", response_model=EngineeringDisclaimer)
async def get_disclaimer():
    """
    Get engineering software disclaimer
    Must be accepted before using the software
    """
    return get_engineering_disclaimer()


@router.post("/disclaimer/accept")
async def accept_disclaimer(
    acceptance: DisclaimerAcceptance,
    request: Request,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Accept engineering disclaimer
    Required before performing any analysis or design
    """
    if not acceptance.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must accept the disclaimer to use this software"
        )
    
    # Create acceptance record
    acceptance_record = create_acceptance_record(
        user_id=current_user.user_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    # In production, save to database
    # db.add(acceptance_record)
    # db.commit()
    
    return {
        "message": "Disclaimer accepted",
        "accepted_at": acceptance_record.accepted_at,
        "version": acceptance_record.disclaimer_version
    }


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """
    Register a new user
    """
    # Check if user exists
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
        "is_active": True,
        "accepted_disclaimer": False,
        "license_number": user.license_number,
        "organization": user.organization
    }
    
    fake_users_db[user.username] = new_user
    
    return UserResponse(
        id=new_user["id"],
        username=new_user["username"],
        email=new_user["email"],
        full_name=new_user["full_name"],
        is_active=new_user["is_active"],
        accepted_disclaimer=new_user["accepted_disclaimer"]
    )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login to get access token
    """
    # Authenticate user
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["id"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: TokenData = Depends(get_current_active_user)):
    """
    Get current user information
    """
    user = fake_users_db.get(current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        full_name=user.get("full_name"),
        is_active=user["is_active"],
        accepted_disclaimer=user.get("accepted_disclaimer", False)
    )


@router.post("/logout")
async def logout(current_user: TokenData = Depends(get_current_active_user)):
    """
    Logout (client should delete token)
    """
    return {"message": "Successfully logged out"}
