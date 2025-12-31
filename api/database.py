"""
Supabase Database Connection Module
"""
from supabase import create_client, Client
from functools import lru_cache
import logging

from config import settings

logger = logging.getLogger(__name__)

_supabase_client: Client = None


def init_database():
    """Initialize Supabase connection"""
    global _supabase_client
    try:
        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")
        raise


def get_supabase() -> Client:
    """Get Supabase client instance"""
    global _supabase_client
    if _supabase_client is None:
        init_database()
    return _supabase_client


def get_service_client() -> Client:
    """Get Supabase client with service role (bypasses RLS)"""
    if not settings.supabase_service_key:
        raise ValueError("SUPABASE_SERVICE_KEY not configured")
    return create_client(
        settings.supabase_url,
        settings.supabase_service_key
    )


class Database:
    """Database helper class with common operations"""
    
    def __init__(self, client: Client = None):
        self.client = client or get_supabase()
    
    # ==========================================
    # TENANT OPERATIONS
    # ==========================================
    
    def get_tenant(self, tenant_id: str):
        """Get tenant by ID"""
        response = self.client.table("tenants").select("*").eq("id", tenant_id).single().execute()
        return response.data
    
    def get_tenant_by_subdomain(self, subdomain: str):
        """Get tenant by subdomain"""
        response = self.client.table("tenants").select("*").eq("subdomain", subdomain).single().execute()
        return response.data
    
    def create_tenant(self, data: dict):
        """Create new tenant"""
        response = self.client.table("tenants").insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_tenant(self, tenant_id: str, data: dict):
        """Update tenant"""
        response = self.client.table("tenants").update(data).eq("id", tenant_id).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # USER OPERATIONS
    # ==========================================
    
    def get_user(self, user_id: str):
        """Get user by ID"""
        response = self.client.table("users").select("*, tenants(*)").eq("id", user_id).single().execute()
        return response.data
    
    def get_user_by_email(self, email: str):
        """Get user by email"""
        response = self.client.table("users").select("*, tenants(*)").eq("email", email).single().execute()
        return response.data
    
    def get_users_by_tenant(self, tenant_id: str):
        """Get all users for a tenant"""
        response = self.client.table("users").select("*").eq("tenant_id", tenant_id).execute()
        return response.data
    
    def create_user(self, data: dict):
        """Create user profile (after Supabase Auth signup)"""
        response = self.client.table("users").insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_user(self, user_id: str, data: dict):
        """Update user"""
        response = self.client.table("users").update(data).eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # JOB OPERATIONS
    # ==========================================
    
    def get_jobs(self, tenant_id: str, status: str = None, limit: int = 100):
        """Get jobs for tenant"""
        query = self.client.table("jobs").select("*, customers(name)").eq("tenant_id", tenant_id)
        if status:
            query = query.eq("status", status)
        response = query.order("created_at", desc=True).limit(limit).execute()
        return response.data
    
    def get_job(self, job_id: str):
        """Get single job"""
        response = self.client.table("jobs").select("*, customers(*)").eq("id", job_id).single().execute()
        return response.data
    
    def create_job(self, data: dict):
        """Create job"""
        response = self.client.table("jobs").insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_job(self, job_id: str, data: dict):
        """Update job"""
        response = self.client.table("jobs").update(data).eq("id", job_id).execute()
        return response.data[0] if response.data else None
    
    def delete_job(self, job_id: str):
        """Delete job (soft delete by archiving)"""
        response = self.client.table("jobs").update({"is_archived": True}).eq("id", job_id).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # COST OPERATIONS
    # ==========================================
    
    def get_weekly_costs(self, job_id: str):
        """Get weekly costs for a job"""
        response = self.client.table("weekly_costs").select("*").eq("job_id", job_id).order("week_ending", desc=True).execute()
        return response.data
    
    def get_weekly_cost(self, job_id: str, week_ending: str):
        """Get specific weekly cost entry"""
        response = self.client.table("weekly_costs").select("*").eq("job_id", job_id).eq("week_ending", week_ending).single().execute()
        return response.data
    
    def upsert_weekly_cost(self, data: dict):
        """Insert or update weekly cost"""
        response = self.client.table("weekly_costs").upsert(
            data, 
            on_conflict="tenant_id,job_id,week_ending"
        ).execute()
        return response.data[0] if response.data else None
    
    def get_job_cost_totals(self, job_id: str):
        """Get aggregated cost totals for a job"""
        response = self.client.rpc("get_job_cost_totals", {"p_job_id": job_id}).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # COST LINE ITEMS
    # ==========================================
    
    def get_cost_line_items(self, job_id: str):
        """Get cost line items for a job"""
        response = self.client.table("cost_line_items").select("*").eq("job_id", job_id).order("date", desc=True).execute()
        return response.data
    
    def create_cost_line_items(self, items: list):
        """Create multiple cost line items"""
        response = self.client.table("cost_line_items").insert(items).execute()
        return response.data
    
    # ==========================================
    # CUSTOMER OPERATIONS
    # ==========================================
    
    def get_customers(self, tenant_id: str, active_only: bool = True):
        """Get customers for tenant"""
        query = self.client.table("customers").select("*").eq("tenant_id", tenant_id)
        if active_only:
            query = query.eq("is_active", True)
        response = query.order("name").execute()
        return response.data
    
    def get_customer(self, customer_id: str):
        """Get single customer"""
        response = self.client.table("customers").select("*").eq("id", customer_id).single().execute()
        return response.data
    
    def create_customer(self, data: dict):
        """Create customer"""
        response = self.client.table("customers").insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_customer(self, customer_id: str, data: dict):
        """Update customer"""
        response = self.client.table("customers").update(data).eq("id", customer_id).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # VENDOR OPERATIONS
    # ==========================================
    
    def get_vendors(self, tenant_id: str, active_only: bool = True):
        """Get vendors for tenant"""
        query = self.client.table("vendors").select("*").eq("tenant_id", tenant_id)
        if active_only:
            query = query.eq("is_active", True)
        response = query.order("name").execute()
        return response.data
    
    def get_vendor(self, vendor_id: str):
        """Get single vendor"""
        response = self.client.table("vendors").select("*").eq("id", vendor_id).single().execute()
        return response.data
    
    def create_vendor(self, data: dict):
        """Create vendor"""
        response = self.client.table("vendors").insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_vendor(self, vendor_id: str, data: dict):
        """Update vendor"""
        response = self.client.table("vendors").update(data).eq("id", vendor_id).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # EMPLOYEE OPERATIONS
    # ==========================================
    
    def get_employees(self, tenant_id: str, active_only: bool = True):
        """Get employees for tenant"""
        query = self.client.table("employees").select("*").eq("tenant_id", tenant_id)
        if active_only:
            query = query.eq("is_active", True)
        response = query.order("last_name").execute()
        return response.data
    
    def get_employee(self, employee_id: str):
        """Get single employee"""
        response = self.client.table("employees").select("*").eq("id", employee_id).single().execute()
        return response.data
    
    def create_employee(self, data: dict):
        """Create employee"""
        response = self.client.table("employees").insert(data).execute()
        return response.data[0] if response.data else None
    
    def update_employee(self, employee_id: str, data: dict):
        """Update employee"""
        response = self.client.table("employees").update(data).eq("id", employee_id).execute()
        return response.data[0] if response.data else None
    
    # ==========================================
    # AUDIT LOG
    # ==========================================
    
    def log_audit(self, tenant_id: str, user_id: str, action: str, 
                  table_name: str, record_id: str = None,
                  old_data: dict = None, new_data: dict = None):
        """Create audit log entry"""
        data = {
            "tenant_id": tenant_id,
            "user_id": user_id,
            "action": action,
            "table_name": table_name,
            "record_id": record_id,
            "old_data": old_data,
            "new_data": new_data
        }
        self.client.table("audit_logs").insert(data).execute()
