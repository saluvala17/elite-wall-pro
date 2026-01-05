"""Customers Router"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import logging

from database import get_supabase, Database
from auth import get_current_user, CurrentUser, require_permission

logger = logging.getLogger(__name__)
router = APIRouter()


class CustomerCreate(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("")
async def list_customers(
    active_only: bool = True,
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all customers"""
    db = Database(get_supabase())
    return db.get_customers(current_user.tenant_id, active_only)


@router.get("/{customer_id}")
async def get_customer(
    customer_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get single customer"""
    db = Database(get_supabase())
    customer = db.get_customer(customer_id)
    if not customer or customer.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("", status_code=201)
async def create_customer(
    data: CustomerCreate,
    current_user: CurrentUser = Depends(require_permission("manage_customers"))
):
    """Create customer"""
    db = Database(get_supabase())
    customer_data = data.model_dump()
    customer_data["tenant_id"] = current_user.tenant_id
    customer_data["created_by"] = current_user.id
    return db.create_customer(customer_data)


@router.patch("/{customer_id}")
async def update_customer(
    customer_id: str,
    data: CustomerUpdate,
    current_user: CurrentUser = Depends(require_permission("manage_customers"))
):
    """Update customer"""
    db = Database(get_supabase())
    existing = db.get_customer(customer_id)
    if not existing or existing.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db.update_customer(customer_id, data.model_dump(exclude_unset=True))


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: str,
    current_user: CurrentUser = Depends(require_permission("manage_customers"))
):
    """Deactivate customer"""
    db = Database(get_supabase())
    existing = db.get_customer(customer_id)
    if not existing or existing.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.update_customer(customer_id, {"is_active": False})
    return {"message": "Customer deactivated"}
