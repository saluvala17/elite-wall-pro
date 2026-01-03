"""Jobs Management Page - Professional SaaS Colors (Fixed Sidebar)"""
import streamlit as st
from datetime import date
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Jobs | Elite Wall Pro", page_icon="📋", layout="wide")

# CRITICAL: Hide Streamlit defaults FIRST
st.markdown(
    """
    <style>
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        header { visibility: hidden !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True
)

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

# Import shared styles and sidebar
from components.shared_styles import get_professional_css
from components.sidebar import render_sidebar

# Get branding
tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#6366F1", "company_name": "Elite Wall Pro"})
primary_color = branding.get("primary_color", "#6366F1")

# CRITICAL: Apply CSS BEFORE rendering sidebar
st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)

# Additional Jobs page-specific CSS
st.markdown(
    f"""
    <style>
    /* ===== Tabs Enhancement ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 44px;
        padding: 0 24px;
        background-color: transparent;
        border-radius: 6px;
        color: var(--gray-600);
        font-weight: 600;
        border: none;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: var(--primary-500) !important;
        color: #ffffff !important;
    }}

    /* ===== Search & Filter Bar ===== */
    .filter-bar {{
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }}

    /* ===== Input Fields ===== */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
        font-size: 0.95rem;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: var(--primary-500);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }}

    .stSelectbox > div > div {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
    }}

    /* ===== Job Expanders ===== */
    .streamlit-expanderHeader {{
        background: #ffffff;
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 16px 20px !important;
        font-weight: 600;
        color: var(--gray-900);
        transition: all 0.2s ease;
    }}

    .streamlit-expanderHeader:hover {{
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        transform: translateY(-1px);
    }}

    div[data-testid="stExpander"] {{
        background: transparent;
        border: none;
        margin-bottom: 12px;
    }}

    .streamlit-expanderContent {{
        background: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
    }}

    /* ===== Status Badges ===== */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
    }}

    .status-active {{
        background: var(--success-light);
        color: var(--success);
    }}

    .status-completed {{
        background: #EFF6FF;
        color: #6366F1;
    }}

    .status-estimate {{
        background: #FEF3C7;
        color: #F59E0B;
    }}

    .status-on_hold {{
        background: var(--gray-100);
        color: var(--gray-600);
    }}

    /* ===== Form Sections ===== */
    .form-section-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--gray-200);
    }}

    /* ===== Number/Text/Date Inputs ===== */
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
    }}

    /* ===== Empty State ===== */
    .empty-state {{
        text-align: center;
        padding: 60px 30px;
        background: #ffffff;
        border-radius: 12px;
        border: 2px dashed var(--gray-300);
    }}

    .empty-state-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}

    .empty-state-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 0.5rem;
    }}

    /* ===== Info Boxes ===== */
    .info-row {{
        background: var(--gray-50);
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .info-label {{
        color: var(--gray-600);
        font-weight: 500;
    }}

    .info-value {{
        color: var(--gray-900);
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# NOW render sidebar (after CSS is loaded)
render_sidebar(branding)

# Header
st.markdown("""
<div class='page-header'>
    <div class='page-title'>📋 Job Management</div>
</div>
""", unsafe_allow_html=True)

api = st.session_state.api_client
user_role = st.session_state.get("user", {}).get("role", "employee")
can_edit = user_role in ("admin", "super_admin", "manager")

# Tabs
if can_edit:
    tab1, tab2 = st.tabs(["📋 All Jobs", "➕ New Job"])
else:
    tab1 = st.tabs(["📋 All Jobs"])[0]

# ==========================================
# ALL JOBS TAB
# ==========================================
with tab1:
    # Enhanced Filter Bar
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Job number or name", label_visibility="collapsed")
    with col2:
        status_filter = st.selectbox("Status", ["All", "active", "estimate", "completed", "on_hold"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    try:
        jobs = api.get_jobs(status=status_filter if status_filter != "All" else None)
        
        if search:
            search_lower = search.lower()
            jobs = [j for j in jobs if 
                search_lower in str(j.get("job_number", "")).lower() or
                search_lower in str(j.get("job_name", "")).lower()
            ]
        
        if not jobs:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>🔍</div>
                <div class='empty-state-title'>No jobs found</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Status icon mapping
            status_icons = {
                "active": "🟢",
                "completed": "🔵",
                "estimate": "🟡",
                "on_hold": "🟠"
            }
            
            status_classes = {
                "active": "status-active",
                "completed": "status-completed",
                "estimate": "status-estimate",
                "on_hold": "status-on_hold"
            }
            
            for job in jobs:
                status = job.get("status", "unknown")
                status_icon = status_icons.get(status, "⚪")
                status_class = status_classes.get(status, "")
                
                with st.expander(f"{status_icon} **{job.get('job_number')}** - {job.get('job_name')}"):
                    # Metrics Row
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Contract", f"${float(job.get('contract_amount', 0) or 0):,.0f}")
                    with col2:
                        st.metric("Total Costs", f"${float(job.get('total_costs', 0) or 0):,.0f}")
                    with col3:
                        variance = float(job.get("variance", 0) or 0)
                        st.metric(
                            "Variance",
                            f"${variance:,.0f}",
                            delta="Under Budget" if variance >= 0 else "Over Budget",
                            delta_color="normal" if variance >= 0 else "inverse"
                        )
                    
                    st.write("")
                    
                    # Info Rows
                    st.markdown(f"""
                    <div class='info-row'>
                        <span class='info-label'>Customer</span>
                        <span class='info-value'>{job.get('customer_name', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class='info-row'>
                        <span class='info-label'>Status</span>
                        <span class='status-badge {status_class}'>{status_icon} {status.replace('_', ' ').title()}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if job.get('start_date'):
                        st.markdown(f"""
                        <div class='info-row'>
                            <span class='info-label'>Start Date</span>
                            <span class='info-value'>{job.get('start_date')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if job.get('end_date'):
                        st.markdown(f"""
                        <div class='info-row'>
                            <span class='info-label'>End Date</span>
                            <span class='info-value'>{job.get('end_date')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if can_edit:
                        st.write("")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✏️ Edit Job", key=f"edit_{job['id']}", use_container_width=True):
                                st.session_state.editing_job_id = job["id"]
                                st.rerun()
    
    except Exception as e:
        st.error(f"⚠️ Error loading jobs: {e}")

# ==========================================
# NEW JOB TAB
# ==========================================
if can_edit:
    with tab2:
        st.markdown('<div class="form-section-title">Create New Job</div>', unsafe_allow_html=True)
        
        try:
            customers = api.get_customers()
        except:
            customers = []
        
        with st.form("create_job"):
            # Basic Information
            st.markdown("### 📋 Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                job_number = st.text_input("Job Number *", placeholder="e.g., 2024-001")
                job_name = st.text_input("Job Name *", placeholder="e.g., Commercial Building Project")
                customer_options = ["Select Customer..."] + [c.get("name", "") for c in customers]
                selected_customer = st.selectbox("Customer", customer_options)
            
            with col2:
                contract_amount = st.number_input("Contract Amount ($)", min_value=0.0, step=1000.0, format="%.2f")
                status = st.selectbox("Status", ["estimate", "active", "on_hold", "completed"])
                
            st.write("")
            
            # Dates & Change Orders
            st.markdown("### 📅 Schedule & Change Orders")
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("Start Date", value=None)
                pending_cos = st.number_input("Pending Change Orders ($)", min_value=0.0, step=100.0, format="%.2f")
            
            with col2:
                end_date = st.date_input("End Date", value=None)
                approved_cos = st.number_input("Approved Change Orders ($)", min_value=0.0, step=100.0, format="%.2f")
            
            st.write("")
            
            # Budget Breakdown
            st.markdown("### 💰 Budget Breakdown")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                budget_insurance = st.number_input("Insurance ($)", min_value=0.0, step=100.0, format="%.2f")
                budget_labor = st.number_input("Labor ($)", min_value=0.0, step=100.0, format="%.2f")
            with col2:
                budget_stamps = st.number_input("Stamps ($)", min_value=0.0, step=100.0, format="%.2f")
                budget_material = st.number_input("Material ($)", min_value=0.0, step=100.0, format="%.2f")
            with col3:
                budget_subs = st.number_input("Subs & Bond ($)", min_value=0.0, step=100.0, format="%.2f")
                budget_equipment = st.number_input("Equipment ($)", min_value=0.0, step=100.0, format="%.2f")
            
            st.write("")
            
            # Notes
            st.markdown("### 📝 Additional Notes")
            notes = st.text_area("Notes", placeholder="Add any relevant notes or comments...", height=100)
            
            st.write("")
            
            # Submit Button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit = st.form_submit_button("➕ Create Job", use_container_width=True, type="primary")
            
            if submit:
                if not job_number or not job_name:
                    st.error("⚠️ Job Number and Name are required")
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
                        st.success("✅ Job created successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Failed to create job: {e}")