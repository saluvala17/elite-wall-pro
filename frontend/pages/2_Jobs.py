"""Jobs Management Page - Enhanced Modern UI"""
import streamlit as st
from datetime import date

st.set_page_config(page_title="Jobs | Elite Wall Pro", page_icon="📋", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#2CA01C", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

# Enhanced Global UI Styling
primary_color = branding.get("primary_color", "#2CA01C")

st.markdown(
    f"""
    <style>
    /* ===== Global Foundation ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #f7f9fc;
        color: #1a1a1a;
    }}

    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1400px !important;
    }}

    /* ===== Page Header ===== */
    .page-header {{
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #e8edf5;
    }}

    .page-title {{
        font-size: 2.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}

    /* ===== Tabs Enhancement ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #e8edf5;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 44px;
        padding: 0 24px;
        background-color: transparent;
        border-radius: 6px;
        color: #64748b;
        font-weight: 600;
        border: none;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {primary_color} !important;
        color: #ffffff !important;
    }}

    /* ===== Search & Filter Bar ===== */
    .filter-bar {{
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e8edf5;
        margin-bottom: 24px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }}

    /* ===== Input Fields ===== */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid #e8edf5;
        padding: 12px 16px;
        font-size: 0.95rem;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {primary_color};
        box-shadow: 0 0 0 3px {primary_color}20;
    }}

    .stSelectbox > div > div {{
        border-radius: 8px;
        border: 1px solid #e8edf5;
    }}

    /* ===== Job Expanders ===== */
    .streamlit-expanderHeader {{
        background: #ffffff;
        border: 1px solid #e8edf5;
        border-radius: 10px;
        padding: 16px 20px !important;
        font-weight: 600;
        color: #0f172a;
        transition: all 0.2s ease;
    }}

    .streamlit-expanderHeader:hover {{
        border-color: {primary_color}40;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transform: translateY(-1px);
    }}

    div[data-testid="stExpander"] {{
        background: transparent;
        border: none;
        margin-bottom: 12px;
    }}

    .streamlit-expanderContent {{
        background: #f8fafc;
        border: 1px solid #e8edf5;
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
        background: #ecfdf5;
        color: #059669;
    }}

    .status-completed {{
        background: #eff6ff;
        color: #2563eb;
    }}

    .status-estimate {{
        background: #fffbeb;
        color: #d97706;
    }}

    .status-on_hold {{
        background: #f3f4f6;
        color: #6b7280;
    }}

    /* ===== Metrics in Expander ===== */
    [data-testid="stMetric"] {{
        background: #ffffff;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #e8edf5;
    }}

    [data-testid="stMetric"] label {{
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }}

    /* ===== Buttons ===== */
    .stButton > button {{
        border-radius: 8px;
        height: 44px;
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}

    .stButton > button[kind="primary"] {{
        background: {primary_color} !important;
        border-color: {primary_color} !important;
    }}

    .stButton > button[kind="secondary"] {{
        background: #ffffff !important;
        border-color: #e8edf5 !important;
        color: #334155 !important;
    }}

    /* ===== Form Sections ===== */
    .form-section {{
        background: #ffffff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid #e8edf5;
        margin-bottom: 20px;
    }}

    .form-section-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid #e8edf5;
    }}

    /* ===== Number Inputs ===== */
    .stNumberInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid #e8edf5;
        padding: 12px 16px;
    }}

    /* ===== Text Areas ===== */
    .stTextArea > div > div > textarea {{
        border-radius: 8px;
        border: 1px solid #e8edf5;
        padding: 12px 16px;
    }}

    /* ===== Date Inputs ===== */
    .stDateInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid #e8edf5;
    }}

    /* ===== Empty State ===== */
    .empty-state {{
        text-align: center;
        padding: 60px 20px;
        background: #ffffff;
        border-radius: 12px;
        border: 2px dashed #e8edf5;
    }}

    .empty-state-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}

    .empty-state-title {{
        font-size: 1.25rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.5rem;
    }}

    /* ===== Info Boxes ===== */
    .info-row {{
        background: #f8fafc;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .info-label {{
        color: #64748b;
        font-weight: 500;
    }}

    .info-value {{
        color: #0f172a;
        font-weight: 600;
    }}

    /* ===== Responsive ===== */
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        
        .page-title {{
            font-size: 1.75rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

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