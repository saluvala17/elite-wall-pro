"""
API Client for Elite Wall Pro Frontend
Handles all communication with the FastAPI backend
"""
import requests
from typing import Optional, Dict, Any, List
import streamlit as st


class APIClient:
    """HTTP client for FastAPI backend"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._token: Optional[str] = None
    
    @property
    def token(self) -> Optional[str]:
        """Get current auth token from session state"""
        return st.session_state.get("access_token")
    
    @token.setter
    def token(self, value: str):
        st.session_state.access_token = value
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers.update(self._headers())
        
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            
            if response.status_code == 401:
                # Token expired or invalid
                st.session_state.authenticated = False
                st.session_state.access_token = None
                st.error("Session expired. Please log in again.")
                st.rerun()
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return None
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            raise Exception(f"API Error: {error_detail}")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to API server")
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    # ==========================================
    # AUTH ENDPOINTS
    # ==========================================
    
    def signin(self, email: str, password: str) -> Dict:
        """Sign in user"""
        response = self._request(
            "POST",
            "/api/v1/auth/signin",
            json={"email": email, "password": password}
        )
        
        if response:
            self.token = response.get("access_token")
            st.session_state.refresh_token = response.get("refresh_token")
            st.session_state.user = response.get("user")
        
        return response
    
    def signup(self, email: str, password: str, name: str, tenant_subdomain: str) -> Dict:
        """Sign up new user"""
        response = self._request(
            "POST",
            "/api/v1/auth/signup",
            json={
                "email": email,
                "password": password,
                "name": name,
                "tenant_subdomain": tenant_subdomain
            }
        )
        
        if response:
            self.token = response.get("access_token")
            st.session_state.user = response.get("user")
        
        return response
    
    def signout(self):
        """Sign out user"""
        try:
            self._request("POST", "/api/v1/auth/signout")
        except:
            pass
        
        self.token = None
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.tenant = None
    
    def get_current_user(self) -> Dict:
        """Get current user profile"""
        return self._request("GET", "/api/v1/auth/me")
    
    # ==========================================
    # TENANT ENDPOINTS
    # ==========================================
    
    def get_tenant(self) -> Dict:
        """Get current tenant"""
        return self._request("GET", "/api/v1/tenants/me")
    
    def update_tenant_branding(self, branding: Dict) -> Dict:
        """Update tenant branding"""
        return self._request("PATCH", "/api/v1/tenants/me/branding", json=branding)
    
    # ==========================================
    # JOB ENDPOINTS
    # ==========================================
    
    def get_jobs(self, status: Optional[str] = None) -> List[Dict]:
        """Get all jobs"""
        params = {}
        if status:
            params["status"] = status
        return self._request("GET", "/api/v1/jobs", params=params) or []
    
    def get_job(self, job_id: str) -> Dict:
        """Get single job"""
        return self._request("GET", f"/api/v1/jobs/{job_id}")
    
    def create_job(self, data: Dict) -> Dict:
        """Create job"""
        return self._request("POST", "/api/v1/jobs", json=data)
    
    def update_job(self, job_id: str, data: Dict) -> Dict:
        """Update job"""
        return self._request("PATCH", f"/api/v1/jobs/{job_id}", json=data)
    
    def delete_job(self, job_id: str) -> Dict:
        """Delete job"""
        return self._request("DELETE", f"/api/v1/jobs/{job_id}")
    
    def get_job_costs(self, job_id: str) -> Dict:
        """Get job cost breakdown"""
        return self._request("GET", f"/api/v1/jobs/{job_id}/costs")
    
    # ==========================================
    # COST ENDPOINTS
    # ==========================================
    
    def get_weekly_costs(self, job_id: str) -> List[Dict]:
        """Get weekly costs for job"""
        return self._request("GET", f"/api/v1/costs/weekly/{job_id}") or []
    
    def save_weekly_cost(self, data: Dict) -> Dict:
        """Save weekly cost"""
        return self._request("POST", "/api/v1/costs/weekly", json=data)
    
    def get_cost_totals(self, job_id: str) -> Dict:
        """Get cost totals"""
        return self._request("GET", f"/api/v1/costs/totals/{job_id}")
    
    def save_cost_line_items(self, items: List[Dict]) -> Dict:
        """Save cost line items"""
        return self._request("POST", "/api/v1/costs/line-items/batch", json={"items": items})
    
    # ==========================================
    # CUSTOMER ENDPOINTS
    # ==========================================
    
    def get_customers(self, active_only: bool = True) -> List[Dict]:
        """Get customers"""
        return self._request("GET", "/api/v1/customers", params={"active_only": active_only}) or []
    
    def get_customer(self, customer_id: str) -> Dict:
        """Get single customer"""
        return self._request("GET", f"/api/v1/customers/{customer_id}")
    
    def create_customer(self, data: Dict) -> Dict:
        """Create customer"""
        return self._request("POST", "/api/v1/customers", json=data)
    
    def update_customer(self, customer_id: str, data: Dict) -> Dict:
        """Update customer"""
        return self._request("PATCH", f"/api/v1/customers/{customer_id}", json=data)
    
    # ==========================================
    # VENDOR ENDPOINTS
    # ==========================================
    
    def get_vendors(self, active_only: bool = True) -> List[Dict]:
        """Get vendors"""
        return self._request("GET", "/api/v1/vendors", params={"active_only": active_only}) or []
    
    def create_vendor(self, data: Dict) -> Dict:
        """Create vendor"""
        return self._request("POST", "/api/v1/vendors", json=data)
    
    def update_vendor(self, vendor_id: str, data: Dict) -> Dict:
        """Update vendor"""
        return self._request("PATCH", f"/api/v1/vendors/{vendor_id}", json=data)
    
    # ==========================================
    # EMPLOYEE ENDPOINTS
    # ==========================================
    
    def get_employees(self, active_only: bool = True) -> List[Dict]:
        """Get employees"""
        return self._request("GET", "/api/v1/employees", params={"active_only": active_only}) or []
    
    def create_employee(self, data: Dict) -> Dict:
        """Create employee"""
        return self._request("POST", "/api/v1/employees", json=data)
    
    def update_employee(self, employee_id: str, data: Dict) -> Dict:
        """Update employee"""
        return self._request("PATCH", f"/api/v1/employees/{employee_id}", json=data)
    
    # ==========================================
    # RECEIPT SCANNING
    # ==========================================
    
    def scan_receipt(self, image_base64: str, job_context: str = None) -> Dict:
        """Scan receipt with AI"""
        return self._request(
            "POST",
            "/api/v1/receipts/scan",
            json={"image_base64": image_base64, "job_context": job_context}
        )
    
    def get_receipt_status(self) -> Dict:
        """Check if receipt scanning is available"""
        return self._request("GET", "/api/v1/receipts/status")
