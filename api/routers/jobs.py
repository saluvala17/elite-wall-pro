"""
Jobs Router
CRUD operations for construction jobs
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
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

class JobCreate(BaseModel):
    job_number: str = Field(..., min_length=1, max_length=50)
    job_name: str = Field(..., min_length=1, max_length=255)
    customer_id: Optional[str] = None
    contract_amount: Decimal = 0
    pending_change_orders: Decimal = 0
    approved_change_orders: Decimal = 0
    budget_insurance: Decimal = 0
    budget_labor: Decimal = 0
    budget_stamps: Decimal = 0
    budget_material: Decimal = 0
    budget_subs_bond: Decimal = 0
    budget_equipment: Decimal = 0
    budget_man_days: int = 0
    status: str = "estimate"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None


class JobUpdate(BaseModel):
    job_number: Optional[str] = None
    job_name: Optional[str] = None
    customer_id: Optional[str] = None
    contract_amount: Optional[Decimal] = None
    pending_change_orders: Optional[Decimal] = None
    approved_change_orders: Optional[Decimal] = None
    budget_insurance: Optional[Decimal] = None
    budget_labor: Optional[Decimal] = None
    budget_stamps: Optional[Decimal] = None
    budget_material: Optional[Decimal] = None
    budget_subs_bond: Optional[Decimal] = None
    budget_equipment: Optional[Decimal] = None
    budget_man_days: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    notes: Optional[str] = None


class JobResponse(BaseModel):
    id: str
    job_number: str
    job_name: str
    customer_id: Optional[str]
    customer_name: Optional[str] = None
    contract_amount: Decimal
    pending_change_orders: Decimal
    approved_change_orders: Decimal
    total_revenue: Decimal = 0
    budget_insurance: Decimal
    budget_labor: Decimal
    budget_stamps: Decimal
    budget_material: Decimal
    budget_subs_bond: Decimal
    budget_equipment: Decimal
    total_budget: Decimal = 0
    budget_man_days: int
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    notes: Optional[str]
    # Calculated fields
    total_costs: Optional[Decimal] = None
    variance: Optional[Decimal] = None
    profit: Optional[Decimal] = None
    profit_margin: Optional[float] = None
    
    class Config:
        from_attributes = True


# ==========================================
# ENDPOINTS
# ==========================================

@router.get("", response_model=List[JobResponse])
async def list_jobs(
    status: Optional[str] = Query(None, description="Filter by status"),
    include_archived: bool = Query(False, description="Include archived jobs"),
    limit: int = Query(100, le=500),
    current_user: CurrentUser = Depends(get_current_user)
):
    """List all jobs for current tenant"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        jobs = db.get_jobs(current_user.tenant_id, status=status, limit=limit)
        
        # Enrich with calculated fields
        result = []
        for job in jobs:
            # Get cost totals
            cost_totals = db.get_job_cost_totals(job["id"])
            
            # Calculate totals
            total_revenue = float(job.get("contract_amount", 0) or 0) + \
                           float(job.get("approved_change_orders", 0) or 0)
            
            total_budget = sum([
                float(job.get("budget_insurance", 0) or 0),
                float(job.get("budget_labor", 0) or 0),
                float(job.get("budget_stamps", 0) or 0),
                float(job.get("budget_material", 0) or 0),
                float(job.get("budget_subs_bond", 0) or 0),
                float(job.get("budget_equipment", 0) or 0),
            ])
            
            total_costs = float(cost_totals.get("total", 0)) if cost_totals else 0
            variance = total_budget - total_costs
            profit = total_revenue - total_costs
            profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
            
            # Get customer name
            customer = job.get("customers", {})
            customer_name = customer.get("name") if customer else None
            
            result.append(JobResponse(
                **job,
                customer_name=customer_name,
                total_revenue=total_revenue,
                total_budget=total_budget,
                total_costs=total_costs,
                variance=variance,
                profit=profit,
                profit_margin=profit_margin
            ))
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list jobs"
        )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get a single job by ID"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        job = db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Verify tenant access
        if job.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get cost totals
        cost_totals = db.get_job_cost_totals(job_id)
        
        # Calculate fields
        total_revenue = float(job.get("contract_amount", 0) or 0) + \
                       float(job.get("approved_change_orders", 0) or 0)
        
        total_budget = sum([
            float(job.get("budget_insurance", 0) or 0),
            float(job.get("budget_labor", 0) or 0),
            float(job.get("budget_stamps", 0) or 0),
            float(job.get("budget_material", 0) or 0),
            float(job.get("budget_subs_bond", 0) or 0),
            float(job.get("budget_equipment", 0) or 0),
        ])
        
        total_costs = float(cost_totals.get("total", 0)) if cost_totals else 0
        
        customer = job.get("customers", {})
        
        return JobResponse(
            **job,
            customer_name=customer.get("name") if customer else None,
            total_revenue=total_revenue,
            total_budget=total_budget,
            total_costs=total_costs,
            variance=total_budget - total_costs,
            profit=total_revenue - total_costs,
            profit_margin=(total_revenue - total_costs) / total_revenue * 100 if total_revenue > 0 else 0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job"
        )


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: CurrentUser = Depends(require_permission("manage_jobs"))
):
    """Create a new job"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        # Prepare data
        data = job_data.model_dump()
        data["tenant_id"] = current_user.tenant_id
        data["created_by"] = current_user.id
        
        # Convert decimals to float for JSON
        for key in data:
            if isinstance(data[key], Decimal):
                data[key] = float(data[key])
            if isinstance(data[key], date):
                data[key] = data[key].isoformat()
        
        # Create job
        job = db.create_job(data)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create job"
            )
        
        # Log audit
        db.log_audit(
            current_user.tenant_id,
            current_user.id,
            "create",
            "jobs",
            job["id"],
            new_data=job
        )
        
        return JobResponse(**job, total_revenue=0, total_budget=0)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job"
        )


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: CurrentUser = Depends(require_permission("manage_jobs"))
):
    """Update an existing job"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        # Get existing job
        existing = db.get_job(job_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Verify tenant
        if existing.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Prepare update data
        update_data = job_data.model_dump(exclude_unset=True)
        
        # Convert types
        for key in update_data:
            if isinstance(update_data[key], Decimal):
                update_data[key] = float(update_data[key])
            if isinstance(update_data[key], date):
                update_data[key] = update_data[key].isoformat()
        
        # Update
        updated = db.update_job(job_id, update_data)
        
        # Log audit
        db.log_audit(
            current_user.tenant_id,
            current_user.id,
            "update",
            "jobs",
            job_id,
            old_data=existing,
            new_data=updated
        )
        
        return JobResponse(**updated, total_revenue=0, total_budget=0)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update job"
        )


@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    current_user: CurrentUser = Depends(require_permission("manage_jobs"))
):
    """Archive a job (soft delete)"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        # Get existing job
        existing = db.get_job(job_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Verify tenant
        if existing.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Soft delete
        db.delete_job(job_id)
        
        # Log audit
        db.log_audit(
            current_user.tenant_id,
            current_user.id,
            "delete",
            "jobs",
            job_id,
            old_data=existing
        )
        
        return {"message": "Job archived successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job"
        )


@router.get("/{job_id}/costs")
async def get_job_costs(
    job_id: str,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get cost breakdown for a job"""
    try:
        supabase = get_supabase()
        db = Database(supabase)
        
        # Verify access
        job = db.get_job(job_id)
        if not job or job.get("tenant_id") != current_user.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Get weekly costs
        weekly_costs = db.get_weekly_costs(job_id)
        
        # Get totals
        totals = db.get_job_cost_totals(job_id)
        
        # Get line items
        line_items = db.get_cost_line_items(job_id)
        
        return {
            "job_id": job_id,
            "totals": totals,
            "weekly_costs": weekly_costs,
            "line_items": line_items,
            "budget": {
                "insurance": job.get("budget_insurance", 0),
                "labor": job.get("budget_labor", 0),
                "stamps": job.get("budget_stamps", 0),
                "material": job.get("budget_material", 0),
                "subs_bond": job.get("budget_subs_bond", 0),
                "equipment": job.get("budget_equipment", 0),
                "man_days": job.get("budget_man_days", 0),
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job costs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job costs"
        )
