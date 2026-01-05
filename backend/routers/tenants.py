"""Tenants Router - For multi-tenant management"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from database import get_supabase, get_service_client, Database
from auth import get_current_user, get_admin_user, get_super_admin_user, CurrentUser

logger = logging.getLogger(__name__)
router = APIRouter()


class TenantCreate(BaseModel):
    name: str
    subdomain: str
    branding: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, Any]] = None
    subscription_tier: str = "basic"


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    branding: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, Any]] = None
    subscription_tier: Optional[str] = None
    subscription_status: Optional[str] = None
    is_active: Optional[bool] = None


class TenantBrandingUpdate(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    logo_url: Optional[str] = None
    company_name: Optional[str] = None


@router.get("/me")
async def get_current_tenant(current_user: CurrentUser = Depends(get_current_user)):
    """Get current user's tenant"""
    db = Database(get_supabase())
    tenant = db.get_tenant(current_user.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.patch("/me/branding")
async def update_tenant_branding(
    branding: TenantBrandingUpdate,
    current_user: CurrentUser = Depends(get_admin_user)
):
    """Update tenant branding (admin only)"""
    db = Database(get_supabase())
    tenant = db.get_tenant(current_user.tenant_id)
    
    current_branding = tenant.get("branding", {})
    updates = branding.model_dump(exclude_unset=True)
    current_branding.update(updates)
    
    db.update_tenant(current_user.tenant_id, {"branding": current_branding})
    return {"message": "Branding updated", "branding": current_branding}


@router.get("/me/users")
async def list_tenant_users(current_user: CurrentUser = Depends(get_admin_user)):
    """List all users in tenant (admin only)"""
    db = Database(get_supabase())
    return db.get_users_by_tenant(current_user.tenant_id)


# Super admin endpoints for managing all tenants
@router.get("")
async def list_all_tenants(current_user: CurrentUser = Depends(get_super_admin_user)):
    """List all tenants (super admin only)"""
    supabase = get_service_client()
    response = supabase.table("tenants").select("*").execute()
    return response.data


@router.post("", status_code=201)
async def create_tenant(
    data: TenantCreate,
    current_user: CurrentUser = Depends(get_super_admin_user)
):
    """Create new tenant (super admin only)"""
    try:
        supabase = get_service_client()
        
        # Check subdomain uniqueness
        existing = supabase.table("tenants").select("id").eq("subdomain", data.subdomain).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Subdomain already exists")
        
        tenant_data = {
            "name": data.name,
            "subdomain": data.subdomain,
            "branding": data.branding or {"primary_color": "#4A7C59", "company_name": data.name},
            "features": data.features or {"receipt_scanning": True, "reports": True, "max_users": 10},
            "subscription_tier": data.subscription_tier
        }
        
        response = supabase.table("tenants").insert(tenant_data).execute()
        return response.data[0] if response.data else None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating tenant: {e}")
        raise HTTPException(status_code=500, detail="Failed to create tenant")


@router.patch("/{tenant_id}")
async def update_tenant(
    tenant_id: str,
    data: TenantUpdate,
    current_user: CurrentUser = Depends(get_super_admin_user)
):
    """Update tenant (super admin only)"""
    supabase = get_service_client()
    update_data = data.model_dump(exclude_unset=True)
    response = supabase.table("tenants").update(update_data).eq("id", tenant_id).execute()
    return response.data[0] if response.data else None


@router.delete("/{tenant_id}")
async def deactivate_tenant(
    tenant_id: str,
    current_user: CurrentUser = Depends(get_super_admin_user)
):
    """Deactivate tenant (super admin only)"""
    supabase = get_service_client()
    supabase.table("tenants").update({"is_active": False}).eq("id", tenant_id).execute()
    return {"message": "Tenant deactivated"}
