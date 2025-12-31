"""
Authentication and Authorization Module
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging

from database import get_supabase, Database
from config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer()


class CurrentUser:
    """Current authenticated user context"""
    def __init__(self, user_data: dict, tenant_data: dict = None):
        self.id = user_data.get("id")
        self.email = user_data.get("email")
        self.name = user_data.get("name")
        self.role = user_data.get("role", "employee")
        self.tenant_id = user_data.get("tenant_id")
        self.tenant = tenant_data
        self.is_active = user_data.get("is_active", True)
        self.raw_data = user_data
    
    @property
    def is_admin(self) -> bool:
        return self.role in ("admin", "super_admin")
    
    @property
    def is_super_admin(self) -> bool:
        return self.role == "super_admin"
    
    def can(self, permission: str) -> bool:
        """Check if user has permission"""
        role_permissions = {
            "super_admin": ["*"],
            "admin": [
                "manage_users", "manage_jobs", "manage_costs",
                "manage_customers", "manage_vendors", "manage_employees",
                "view_reports", "manage_settings"
            ],
            "manager": [
                "manage_jobs", "manage_costs", "manage_customers",
                "manage_vendors", "manage_employees", "view_reports"
            ],
            "employee": [
                "view_jobs", "edit_costs", "view_reports"
            ],
            "viewer": [
                "view_jobs", "view_reports"
            ]
        }
        
        permissions = role_permissions.get(self.role, [])
        return "*" in permissions or permission in permissions


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Validate JWT token and return current user.
    Uses Supabase Auth to validate the token.
    """
    token = credentials.credentials
    
    try:
        # Validate token with Supabase
        supabase = get_supabase()
        
        # Get user from token
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        auth_user = user_response.user
        
        # Get user profile from our users table
        db = Database(supabase)
        user_profile = db.get_user(auth_user.id)
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User profile not found"
            )
        
        if not user_profile.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Get tenant info
        tenant_data = user_profile.get("tenants")
        
        return CurrentUser(user_profile, tenant_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


async def get_current_active_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """Ensure user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return current_user


async def get_admin_user(
    current_user: CurrentUser = Depends(get_current_active_user)
) -> CurrentUser:
    """Ensure user is admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_super_admin_user(
    current_user: CurrentUser = Depends(get_current_active_user)
) -> CurrentUser:
    """Ensure user is super admin"""
    if not current_user.is_super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user


def require_permission(permission: str):
    """Decorator to require specific permission"""
    async def permission_checker(
        current_user: CurrentUser = Depends(get_current_active_user)
    ) -> CurrentUser:
        if not current_user.can(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    return permission_checker


# Optional: API Key authentication for external integrations
async def get_api_key_user(
    x_api_key: Optional[str] = Header(None)
) -> Optional[CurrentUser]:
    """
    Validate API key for external integrations.
    Returns None if no API key provided.
    """
    if not x_api_key:
        return None
    
    try:
        supabase = get_supabase()
        
        # Hash the API key and look it up
        import hashlib
        key_hash = hashlib.sha256(x_api_key.encode()).hexdigest()
        
        response = supabase.table("api_keys").select(
            "*, users(*)"
        ).eq("key_hash", key_hash).eq("is_active", True).single().execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        api_key = response.data
        user_data = api_key.get("users", {})
        
        # Update last used
        supabase.table("api_keys").update(
            {"last_used_at": "now()"}
        ).eq("id", api_key["id"]).execute()
        
        return CurrentUser(user_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API key validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key validation failed"
        )
