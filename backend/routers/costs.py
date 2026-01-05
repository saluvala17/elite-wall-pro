"""
Costs Router
Weekly cost entry and line items
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal
import logging

from database import get_supabase, Database
from auth import get_current_user, CurrentUser, require_permission

logger = logging.getLogger(__name__)
router = APIRouter()


# ==========================================
# MODELS
# ==========================================

class WeeklyCostCreate(BaseModel):
    job_id: str
    week_ending: date
    insurance_actual: Decimal = 0
    labor_actual: Decimal = 0
    stamps_actual: Decimal = 0
    material_actual: Decimal = 0
    subs_bond_actual: Decimal = 0
    equipment_actual: Decimal = 0
    man_days_actual: int = 0
    notes: Optional[str] = None


class CostLineItemCreate(BaseModel):
    job_id: str
    weekly_cost_id: Optional[str] = None
    date: Optional[date] = None
    vendor_name: Optional[str] = None
    description: Optional[str] = None
    category: str = "material"
    amount: Decimal
    receipt_number: Optional[str] = None
    notes: Optional[str] = None


class CostLineItemBatch(BaseModel):
    items: List[CostLineItemCreate]


# ==========================================
# WEEKLY COSTS ENDPOINTS
# ==========================================

@router.get("/weekly/{job_id}")
async def get_weekly_costs(
    job_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get all weekly costs for a job"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        job = db.get_job(job_id)
        if not job or job.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return db.get_weekly_costs(job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get weekly costs")


@router.post("/weekly")
async def upsert_weekly_cost(
    cost_data: WeeklyCostCreate,
    current_user: CurrentUser = Depends(require_permission("manage_costs"))
):
    """Create or update weekly cost entry"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        job = db.get_job(cost_data.job_id)
        if not job or job.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="Job not found")
        
        data = cost_data.model_dump()
        data["tenant_id"] = current_user.tenant_id
        data["created_by"] = current_user.id
        data["week_ending"] = data["week_ending"].isoformat()
        
        for key in data:
            if isinstance(data[key], Decimal):
                data[key] = float(data[key])
        
        return db.upsert_weekly_cost(data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save weekly cost")


@router.post("/line-items/batch")
async def create_cost_line_items_batch(
    batch_data: CostLineItemBatch,
    current_user: CurrentUser = Depends(require_permission("manage_costs"))
):
    """Create multiple cost line items"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        if not batch_data.items:
            return {"created": 0}
        
        job_id = batch_data.items[0].job_id
        job = db.get_job(job_id)
        if not job or job.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="Job not found")
        
        items = []
        for item in batch_data.items:
            data = item.model_dump()
            data["tenant_id"] = current_user.tenant_id
            data["created_by"] = current_user.id
            if data.get("date"):
                data["date"] = data["date"].isoformat()
            if isinstance(data.get("amount"), Decimal):
                data["amount"] = float(data["amount"])
            items.append(data)
        
        result = supabase.table("cost_line_items").insert(items).execute()
        return {"created": len(result.data) if result.data else 0}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create line items")


@router.get("/totals/{job_id}")
async def get_job_cost_totals(
    job_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get aggregated cost totals for a job"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        job = db.get_job(job_id)
        if not job or job.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="Job not found")
        
        totals = db.get_job_cost_totals(job_id)
        
        budget = {
            "insurance": float(job.get("budget_insurance", 0) or 0),
            "labor": float(job.get("budget_labor", 0) or 0),
            "stamps": float(job.get("budget_stamps", 0) or 0),
            "material": float(job.get("budget_material", 0) or 0),
            "subs_bond": float(job.get("budget_subs_bond", 0) or 0),
            "equipment": float(job.get("budget_equipment", 0) or 0),
        }
        budget["total"] = sum(budget.values())
        
        actual = totals or {"insurance": 0, "labor": 0, "stamps": 0, "material": 0, "subs_bond": 0, "equipment": 0, "total": 0}
        
        return {
            "actual": actual,
            "budget": budget,
            "variance": {k: budget.get(k, 0) - float(actual.get(k, 0)) for k in budget}
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get totals")
