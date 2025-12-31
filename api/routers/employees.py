"""Employees Router"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from decimal import Decimal
import logging

from database import get_supabase, Database
from auth import get_current_user, CurrentUser, require_permission

logger = logging.getLogger(__name__)
router = APIRouter()


class EmployeeCreate(BaseModel):
    employee_id: Optional[str] = None
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    hire_date: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class EmployeeUpdate(BaseModel):
    employee_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    hire_date: Optional[date] = None
    termination_date: Optional[date] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("")
async def list_employees(
    active_only: bool = True,
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all employees"""
    db = Database(get_supabase())
    return db.get_employees(current_user.tenant_id, active_only)


@router.get("/{employee_id}")
async def get_employee(
    employee_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get single employee"""
    db = Database(get_supabase())
    employee = db.get_employee(employee_id)
    if not employee or employee.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("", status_code=201)
async def create_employee(
    data: EmployeeCreate,
    current_user: CurrentUser = Depends(require_permission("manage_employees"))
):
    """Create employee"""
    db = Database(get_supabase())
    emp_data = data.model_dump()
    emp_data["tenant_id"] = current_user.tenant_id
    emp_data["created_by"] = current_user.id
    
    # Convert types
    if emp_data.get("hourly_rate"):
        emp_data["hourly_rate"] = float(emp_data["hourly_rate"])
    if emp_data.get("hire_date"):
        emp_data["hire_date"] = emp_data["hire_date"].isoformat()
    
    return db.create_employee(emp_data)


@router.patch("/{employee_id}")
async def update_employee(
    employee_id: str,
    data: EmployeeUpdate,
    current_user: CurrentUser = Depends(require_permission("manage_employees"))
):
    """Update employee"""
    db = Database(get_supabase())
    existing = db.get_employee(employee_id)
    if not existing or existing.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Convert types
    if update_data.get("hourly_rate"):
        update_data["hourly_rate"] = float(update_data["hourly_rate"])
    for date_field in ["hire_date", "termination_date"]:
        if update_data.get(date_field):
            update_data[date_field] = update_data[date_field].isoformat()
    
    return db.update_employee(employee_id, update_data)


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    current_user: CurrentUser = Depends(require_permission("manage_employees"))
):
    """Deactivate employee"""
    db = Database(get_supabase())
    existing = db.get_employee(employee_id)
    if not existing or existing.get("tenant_id") != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.update_employee(employee_id, {"is_active": False})
    return {"message": "Employee deactivated"}
