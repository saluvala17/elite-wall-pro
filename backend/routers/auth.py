"""
Authentication Router
Handles login, signup, password reset, etc.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

from database import get_supabase, Database
from auth import get_current_user, CurrentUser

logger = logging.getLogger(__name__)
router = APIRouter()


# ==========================================
# REQUEST/RESPONSE MODELS
# ==========================================

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    tenant_subdomain: str  # Which tenant to join


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordUpdateRequest(BaseModel):
    new_password: str


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


# ==========================================
# ENDPOINTS
# ==========================================

@router.post("/signup", response_model=TokenResponse)
async def sign_up(request: SignUpRequest):
    """
    Sign up a new user.
    User must specify which tenant (by subdomain) they're joining.
    """
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        # Find tenant by subdomain
        tenant = db.get_tenant_by_subdomain(request.tenant_subdomain)
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{request.tenant_subdomain}' not found"
            )
        
        if not tenant.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Organization is not active"
            )
        
        # Create user in Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        # Create user profile in our table
        user_profile = db.create_user({
            "id": auth_response.user.id,
            "tenant_id": tenant["id"],
            "email": request.email,
            "name": request.name,
            "role": "employee"  # Default role
        })
        
        return TokenResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            expires_in=auth_response.session.expires_in,
            user={
                "id": auth_response.user.id,
                "email": request.email,
                "name": request.name,
                "tenant_id": tenant["id"],
                "tenant_name": tenant["name"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Signup failed"
        )


@router.post("/signin", response_model=TokenResponse)
async def sign_in(request: SignInRequest):
    """Sign in an existing user"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        # Sign in with Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if not auth_response.user or not auth_response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Get user profile
        user_profile = db.get_user(auth_response.user.id)
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        if not user_profile.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Update last login
        db.update_user(auth_response.user.id, {"last_login_at": "now()"})
        
        tenant = user_profile.get("tenants", {})
        
        return TokenResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            expires_in=auth_response.session.expires_in,
            user={
                "id": auth_response.user.id,
                "email": user_profile["email"],
                "name": user_profile["name"],
                "role": user_profile["role"],
                "tenant_id": user_profile["tenant_id"],
                "tenant_name": tenant.get("name", ""),
                "branding": tenant.get("branding", {})
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signin error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.post("/signout")
async def sign_out(current_user: CurrentUser = Depends(get_current_user)):
    """Sign out current user"""
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
        return {"message": "Signed out successfully"}
    except Exception as e:
        logger.error(f"Signout error: {e}")
        return {"message": "Signed out"}


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    try:
        supabase = get_supabase()
        response = supabase.auth.refresh_session(refresh_token)
        
        if not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.post("/password-reset")
async def request_password_reset(request: PasswordResetRequest):
    """Request password reset email"""
    try:
        supabase = get_supabase()
        supabase.auth.reset_password_email(request.email)
        return {"message": "Password reset email sent if account exists"}
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        # Don't reveal if email exists
        return {"message": "Password reset email sent if account exists"}


@router.get("/me")
async def get_current_user_profile(current_user: CurrentUser = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "tenant_id": current_user.tenant_id,
        "tenant": current_user.tenant
    }


@router.patch("/me")
async def update_current_user_profile(
    updates: UserProfileUpdate,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Update current user profile"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        update_data = updates.model_dump(exclude_unset=True)
        
        if update_data:
            db.update_user(current_user.id, update_data)
        
        return {"message": "Profile updated successfully"}
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
