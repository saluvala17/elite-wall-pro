"""Jobs Management Page"""
import streamlit as st
from datetime import date

st.set_page_config(page_title="Jobs | Elite Wall Pro", page_icon="📋", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

st.title("📋 Job Management")

api = st.session_state.api_client
user_role = st.session_state.get("user", {}).get("role", "employee")
can_edit = user_role in ("admin", "super_admin", "manager")

# Tabs
if can_edit:
    tab1, tab2 = st.tabs(["📋 All Jobs", "➕ New Job"])
else:
    tab1 = st.tabs(["📋 All Jobs"])[0]

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Job number or name")
    with col2:
        status_filter = st.selectbox("Status", ["All", "active", "estimate", "completed", "on_hold"])
    
    try:
        jobs = api.get_jobs(status=status_filter if status_filter != "All" else None)
        
        if search:
            search_lower = search.lower()
            jobs = [j for j in jobs if 
                search_lower in str(j.get("job_number", "")).lower() or
                search_lower in str(j.get("job_name", "")).lower()
            ]
        
        if not jobs:
            st.info("No jobs found")
        else:
            for job in jobs:
                status = job.get("status", "unknown")
                status_icon = {"active": "🟢", "completed": "🔵", "estimate": "🟡", "on_hold": "🟠"}.get(status, "⚪")
                
                with st.expander(f"{status_icon} {job.get('job_number')} - {job.get('job_name')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Contract", f"${float(job.get('contract_amount', 0) or 0):,.0f}")
                    with col2:
                        st.metric("Total Costs", f"${float(job.get('total_costs', 0) or 0):,.0f}")
                    with col3:
                        variance = float(job.get("variance", 0) or 0)
                        st.metric("Variance", f"${variance:,.0f}", 
                                 delta="Under" if variance >= 0 else "Over",
                                 delta_color="normal" if variance >= 0 else "inverse")
                    
                    st.write(f"**Customer:** {job.get('customer_name', 'N/A')}")
                    st.write(f"**Status:** {status.title()}")
                    
                    if can_edit:
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✏️ Edit", key=f"edit_{job['id']}"):
                                st.session_state.editing_job_id = job["id"]
                                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading jobs: {e}")

if can_edit:
    with tab2:
        st.subheader("Create New Job")
        
        try:
            customers = api.get_customers()
        except:
            customers = []
        
        with st.form("create_job"):
            col1, col2 = st.columns(2)
            
            with col1:
                job_number = st.text_input("Job Number *")
                job_name = st.text_input("Job Name *")
                customer_options = ["Select Customer..."] + [c.get("name", "") for c in customers]
                selected_customer = st.selectbox("Customer", customer_options)
                contract_amount = st.number_input("Contract Amount ($)", min_value=0.0, step=1000.0)
                status = st.selectbox("Status", ["estimate", "active", "on_hold", "completed"])
            
            with col2:
                start_date = st.date_input("Start Date", value=None)
                end_date = st.date_input("End Date", value=None)
                pending_cos = st.number_input("Pending COs ($)", min_value=0.0, step=100.0)
                approved_cos = st.number_input("Approved COs ($)", min_value=0.0, step=100.0)
            
            st.subheader("Budget Breakdown")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                budget_insurance = st.number_input("Insurance ($)", min_value=0.0, step=100.0)
                budget_labor = st.number_input("Labor ($)", min_value=0.0, step=100.0)
            with col2:
                budget_stamps = st.number_input("Stamps ($)", min_value=0.0, step=100.0)
                budget_material = st.number_input("Material ($)", min_value=0.0, step=100.0)
            with col3:
                budget_subs = st.number_input("Subs & Bond ($)", min_value=0.0, step=100.0)
                budget_equipment = st.number_input("Equipment ($)", min_value=0.0, step=100.0)
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("➕ Create Job", use_container_width=True, type="primary"):
                if not job_number or not job_name:
                    st.error("Job Number and Name are required")
                else:
                    # Find customer ID
                    customer_id = None
                    if selected_customer != "Select Customer...":
                        for c in customers:
                            if c.get("name") == selected_customer:
                                customer_id = c.get("id")
                                break
                    
                    job_data = {
                        "job_number": job_number,
                        "job_name": job_name,
                        "customer_id": customer_id,
                        "contract_amount": contract_amount,
                        "pending_change_orders": pending_cos,
                        "approved_change_orders": approved_cos,
                        "status": status,
                        "start_date": start_date.isoformat() if start_date else None,
                        "end_date": end_date.isoformat() if end_date else None,
                        "budget_insurance": budget_insurance,
                        "budget_labor": budget_labor,
                        "budget_stamps": budget_stamps,
                        "budget_material": budget_material,
                        "budget_subs_bond": budget_subs,
                        "budget_equipment": budget_equipment,
                        "notes": notes
                    }
                    
                    try:
                        api.create_job(job_data)
                        st.success("Job created!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Failed to create job: {e}")
