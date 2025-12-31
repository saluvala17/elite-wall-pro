"""
Elite Wall Pro - Streamlit Frontend
Modernized UI Version
"""
import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from api_client import APIClient
from components.auth import render_login_page, check_auth, logout
from components.sidebar import render_sidebar

# Page configuration
st.set_page_config(
    page_title="Elite Wall Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state (Functionality unchanged)
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(settings.api_url)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "tenant" not in st.session_state:
    st.session_state.tenant = None

def get_branding():
    if st.session_state.tenant:
        branding = st.session_state.tenant.get("branding", {})
        return {
            "primary_color": branding.get("primary_color", "#2E5BFF"),
            "secondary_color": branding.get("secondary_color", "#8B4513"),
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url")
        }
    return {
        "primary_color": "#2E5BFF",
        "secondary_color": "#8B4513",
        "company_name": "Elite Wall Pro",
        "logo_url": None
    }

def apply_custom_css(branding):
    primary = branding["primary_color"]
    st.markdown(f"""
    <style>
        @import url('fonts.googleapis.com');
        
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }}

        /* Header Styling */
        .main-header {{
            font-size: 2.2rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            letter-spacing: -0.025em;
        }}
        
        .sub-header {{
            font-size: 1.1rem;
            color: #64748b;
            margin-bottom: 2rem;
        }}

        /* KPI Card Styling */
        div[data-testid="stMetric"] {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #f1f5f9;
        }}
        
        /* Modern Button Styling */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
            height: 3rem;
            border: none;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        /* Custom Job Card Table */
        .job-card {{
            background: white;
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 5px solid {primary};
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        /* Hide standard streamlit elements for cleaner look */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Sidebar Polish */
        [data-testid="stSidebar"] {{
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }}
    </style>
    """, unsafe_allow_html=True)

def main():
    if not check_auth():
        render_login_page()
        return
    
    branding = get_branding()
    apply_custom_css(branding)
    render_sidebar(branding)
    
    # Hero Section
    st.markdown(f'<p class="main-header">Welcome back, {st.session_state.user.get("first_name", "Team")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{branding["company_name"]} • Job Costing Dashboard</p>', unsafe_allow_html=True)
    
    api = st.session_state.api_client
    
    try:
        jobs = api.get_jobs()
        if not jobs:
            st.info("No jobs found. Create your first job to get started!")
            if st.button("➕ Create Job"):
                st.switch_page("pages/2_Jobs.py")
            return
        
        active_jobs = [j for j in jobs if j.get("status") == "active"]
        total_contract = sum(float(j.get("contract_amount", 0) or 0) for j in active_jobs)
        total_costs = sum(float(j.get("total_costs", 0) or 0) for j in active_jobs)
        over_budget = len([j for j in active_jobs if float(j.get("variance", 0) or 0) < 0])
        
        # Dashboard KPIs
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Projects", len(active_jobs), f"{len(jobs)} Total")
        m2.metric("Contract Value", f"${total_contract:,.0f}")
        m3.metric("Total Spend", f"${total_costs:,.0f}")
        m4.metric("Risk Alerts", over_budget, "Attention Required" if over_budget > 0 else "All On Track", 
                  delta_color="inverse" if over_budget > 0 else "normal")
        
        st.write("##") # Spacing

        # Layout for Table and Actions
        col_table, col_actions = st.columns([3, 1])
        
        with col_table:
            st.markdown("### 📋 Active Project Overview")
            
            # Formatted Job List instead of just a raw dataframe
            for job in active_jobs[:6]:
                total_revenue = float(job.get("contract_amount", 0) or 0) + \
                               float(job.get("approved_change_orders", 0) or 0)
                total_cost = float(job.get("total_costs", 0) or 0)
                profit = total_revenue - total_cost
                margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
                status_color = "#ef4444" if float(job.get("variance", 0) or 0) < 0 else "#22c55e"
                
                with st.container():
                    st.markdown(f"""
                    <div class="job-card" style="border-left: 5px solid {status_color}">
                        <div>
                            <small style="color: #64748b;">{job.get('job_number', '')}</small>
                            <div style="font-weight: 600; font-size: 1.1rem;">{job.get('job_name', '')}</div>
                            <small style="color: #94a3b8;">{job.get('customer_name', 'N/A')}</small>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: 700;">${total_cost:,.0f} / <span style="color: #64748b;">${total_revenue:,.0f}</span></div>
                            <div style="color: {status_color}; font-size: 0.85rem; font-weight: 600;">{margin:.1f}% Margin</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with col_actions:
            st.markdown("### ⚡ Actions")
            st.button("➕ Create New Job", use_container_width=True, on_click=lambda: st.switch_page("pages/2_Jobs.py"), type="primary")
            st.button("💰 Log New Costs", use_container_width=True, on_click=lambda: st.switch_page("pages/3_Cost_Entry.py"))
            st.button("📊 View Reports", use_container_width=True, on_click=lambda: st.switch_page("pages/6_Reports.py"))
            st.button("👥 Manage Customers", use_container_width=True, on_click=lambda: st.switch_page("pages/4_Customers.py"))
            
            # Help Card
            st.markdown("""
            <div style="background: #eff6ff; padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px solid #bfdbfe;">
                <p style="color: #1e40af; font-size: 0.8rem; margin: 0;"><strong>Tip:</strong> You have <b>{over_budget}</b> projects currently exceeding their estimated variance.</p>
            </div>
            """.format(over_budget=over_budget), unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        if st.button("🔄 Refresh Data"):
            st.rerun()

if __name__ == "__main__":
    main()
