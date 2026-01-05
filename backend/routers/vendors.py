"""Vendors Router"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

from database import get_supabase, Database
from auth import get_current_user, CurrentUser, require_permission

logger = logging.getLogger(__name__)
router = APIRouter()


class VendorCreate(BaseModel):
    name: str
    vendor_type: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None
    tax_id: Optional[str] = None


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    vendor_type: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None
    tax_id: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("")
async def list_vendors(
    active_only: bool = True,
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all vendors"""
    db = Database(get_supabase())
    return db.get_vendors(current_user.tenant_id, active_only)


@router.get("/{vendor_id}")
async def get_vendor(
    vendor_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get single vendor"""
    db = Database(get_supabase())
    vendor = db.get_vendor(vendor_id)
    if not vendor or vendor.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.post("", status_code=201)
async def create_vendor(
    data: VendorCreate,
    current_user: CurrentUser = Depends(require_permission("manage_vendors"))
):
    """Create vendor"""
    db = Database(get_supabase())
    vendor_data = data.model_dump()
    vendor_data["tenant_id"] = current_user.tenant_id
    vendor_data["created_by"] = current_user.id
    return db.create_vendor(vendor_data)


@router.patch("/{vendor_id}")
async def update_vendor(
    vendor_id: str,
    data: VendorUpdate,
    current_user: CurrentUser = Depends(require_permission("manage_vendors"))
):
    """Update vendor"""
    db = Database(get_supabase())
    existing = db.get_vendor(vendor_id)
    if not existing or existing.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db.update_vendor(vendor_id, data.model_dump(exclude_unset=True))


@router.delete("/{vendor_id}")
async def delete_vendor(
    vendor_id: str,
    current_user: CurrentUser = Depends(require_permission("manage_vendors"))
):
    """Deactivate vendor"""
    db = Database(get_supabase())
    existing = db.get_vendor(vendor_id)
    if not existing or existing.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.update_vendor(vendor_id, {"is_active": False})
    return {"message": "Vendor deactivated"}
