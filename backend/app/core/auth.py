"""
Authentication and Authorization System
Implements RBAC, API rate limiting, and session management
"""
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
import logging
from enum import Enum
# SECURITY FIX: Use timezone-aware datetime
from app.core.datetime_utils import utc_now

logger = logging.getLogger(__name__)

# Configuration
import os
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-use-env-variable")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserRole(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    ENGINEER = "engineer"
    VIEWER = "viewer"
    GUEST = "guest"


class Permission(str, Enum):
    """Permissions for fine-grained access control"""
    # Project permissions
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    PROJECT_SHARE = "project:share"
    
    # Model permissions
    MODEL_CREATE = "model:create"
    MODEL_READ = "model:read"
    MODEL_UPDATE = "model:update"
    MODEL_DELETE = "model:delete"
    
    # Analysis permissions
    ANALYSIS_RUN = "analysis:run"
    ANALYSIS_READ = "analysis:read"
    
    # Design permissions
    DESIGN_RUN = "design:run"
    DESIGN_READ = "design:read"
    
    # Admin permissions
    USER_MANAGE = "user:manage"
    SETTINGS_MANAGE = "settings:manage"


# Role-Permission mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [p for p in Permission],  # All permissions
    UserRole.ENGINEER: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_SHARE,
        Permission.MODEL_CREATE,
        Permission.MODEL_READ,
        Permission.MODEL_UPDATE,
        Permission.MODEL_DELETE,
        Permission.ANALYSIS_RUN,
        Permission.ANALYSIS_READ,
        Permission.DESIGN_RUN,
        Permission.DESIGN_READ,
    ],
    UserRole.VIEWER: [
        Permission.PROJECT_READ,
        Permission.MODEL_READ,
        Permission.ANALYSIS_READ,
        Permission.DESIGN_READ,
    ],
    UserRole.GUEST: [
        Permission.PROJECT_READ,
        Permission.MODEL_READ,
    ]
}


class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None
    permissions: List[Permission] = []


class User(BaseModel):
    """User model"""
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None


class UserCreate(BaseModel):
    """User creation model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    role: UserRole = UserRole.VIEWER


class UserInDB(User):
    """User model with hashed password"""
    hashed_password: str


class ProjectPermission(BaseModel):
    """Project-level permissions"""
    project_id: int
    user_id: int
    role: UserRole
    can_read: bool = True
    can_write: bool = False
    can_delete: bool = False
    can_share: bool = False


# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


# Token utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    # SECURITY FIX: Use timezone-aware datetime
    if expires_delta:
        expire = utc_now() + expires_delta
    else:
        expire = utc_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    # SECURITY FIX: Use timezone-aware datetime
    expire = utc_now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get permissions for role
        permissions = ROLE_PERMISSIONS.get(UserRole(role), [])
        
        return TokenData(
            username=username,
            user_id=user_id,
            role=UserRole(role) if role else None,
            permissions=permissions
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Dependency for getting current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Get current authenticated user from token"""
    return decode_token(token)


async def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Get current active user"""
    # In production, check if user is active in database
    return current_user


# Permission checking
def require_permission(permission: Permission):
    """Dependency to require specific permission"""
    async def permission_checker(current_user: TokenData = Depends(get_current_active_user)):
        if permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {permission}"
            )
        return current_user
    return permission_checker


def require_role(role: UserRole):
    """Dependency to require specific role"""
    async def role_checker(current_user: TokenData = Depends(get_current_active_user)):
        if current_user.role != role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {role}"
            )
        return current_user
    return role_checker


# Rate limiting
class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests: int = 100, window: int = 60):
        """
        Initialize rate limiter
        
        Args:
            requests: Maximum requests allowed
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.clients = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make request"""
        # SECURITY FIX: Use timezone-aware datetime
        now = utc_now()
        
        if client_id not in self.clients:
            self.clients[client_id] = []
        
        # Remove old requests outside window
        self.clients[client_id] = [
            req_time for req_time in self.clients[client_id]
            if (now - req_time).total_seconds() < self.window
        ]
        
        # Check if limit exceeded
        if len(self.clients[client_id]) >= self.requests:
            return False
        
        # Add current request
        self.clients[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        if client_id not in self.clients:
            return self.requests
        
        # SECURITY FIX: Use timezone-aware datetime
        now = utc_now()
        recent_requests = [
            req_time for req_time in self.clients[client_id]
            if (now - req_time).total_seconds() < self.window
        ]
        
        return max(0, self.requests - len(recent_requests))


# Global rate limiter instance
rate_limiter = RateLimiter(requests=100, window=60)


async def check_rate_limit(request: Request):
    """Dependency to check rate limit"""
    client_id = request.client.host
    
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            headers={"Retry-After": str(rate_limiter.window)}
        )
    
    return True


# Audit logging
class AuditLog(BaseModel):
    """Audit log entry"""
    timestamp: datetime
    user_id: Optional[int]
    username: Optional[str]
    action: str
    resource_type: str
    resource_id: Optional[str]
    ip_address: str
    user_agent: Optional[str]
    status: str  # success, failure
    details: Optional[dict] = None


def log_audit_event(
    user: TokenData,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    status: str = "success",
    details: Optional[dict] = None,
    request: Optional[Request] = None
):
    """Log an audit event"""
    log_entry = AuditLog(
        # SECURITY FIX: Use timezone-aware datetime
        timestamp=utc_now(),
        user_id=user.user_id,
        username=user.username,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=request.client.host if request else "unknown",
        user_agent=request.headers.get("user-agent") if request else None,
        status=status,
        details=details
    )
    
    # In production, save to database
    logger.info(f"AUDIT: {log_entry.dict()}")
    
    return log_entry
