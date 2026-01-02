"""
Elite Wall Pro - Streamlit Frontend
Professional QuickBooks-Style UI with Contractor-Friendly Sidebar
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from api_client import APIClient
from components.auth import render_login_page, check_auth
from components.sidebar import render_sidebar

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Elite Wall Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Hide Streamlit Defaults (Clean SaaS Look)
# --------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Session State Initialization (UNCHANGED)
# --------------------------------------------------
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(settings.api_url)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "tenant" not in st.session_state:
    st.session_state.tenant = None


# --------------------------------------------------
# Branding Helper
# --------------------------------------------------
def get_branding():
    if st.session_state.tenant:
        branding = st.session_state.tenant.get("branding", {})
        return {
            "primary_color": branding.get("primary_color", "#2CA01C"),
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url"),
        }
    return {
        "primary_color": "#2CA01C",
        "company_name": "Elite Wall Pro",
        "logo_url": None,
    }


# --------------------------------------------------
# Enhanced Global UI Styling (Modern QuickBooks)
# --------------------------------------------------
def apply_global_css(primary_color: str):
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

        /* Remove default Streamlit padding */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            max-width: 1400px !important;
        }}

        /* ===== Enhanced Sidebar Styling (QuickBooks Style) ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #1e3a2e 0%, #163025 100%);
            border-right: none;
            box-shadow: 4px 0 16px rgba(0, 0, 0, 0.1);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: transparent;
            padding-top: 2rem;
        }}

        /* Sidebar Company Header */
        .sidebar-header {{
            background: rgba(255, 255, 255, 0.08);
            padding: 20px 16px;
            margin: 0 16px 24px 16px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .sidebar-company-name {{
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }}

        .sidebar-company-icon {{
            background: {primary_color};
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
        }}

        .sidebar-user-info {{
            background: rgba(255, 255, 255, 0.05);
            padding: 10px 12px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .sidebar-user-name {{
            color: #ffffff;
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 4px;
        }}

        .sidebar-user-role {{
            color: rgba(255, 255, 255, 0.65);
            font-size: 0.8rem;
            text-transform: capitalize;
        }}

        /* Sidebar Navigation Section */
        .sidebar-nav-section {{
            margin: 0 8px 20px 8px;
        }}

        .sidebar-nav-title {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 8px 12px 8px 12px;
            margin-bottom: 4px;
        }}

        /* Override Streamlit's button styling in sidebar */
        [data-testid="stSidebar"] .stButton {{
            margin-bottom: 4px;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            background: transparent;
            border: 1px solid transparent;
            color: rgba(255, 255, 255, 0.85);
            text-align: left;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.2s ease;
            height: auto;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 10px;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.12);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateX(2px);
            box-shadow: none;
        }}

        [data-testid="stSidebar"] .stButton > button:active {{
            background: {primary_color};
            color: #ffffff;
            border-color: {primary_color};
            box-shadow: 0 2px 8px rgba(44, 160, 28, 0.3);
        }}

        /* Logout button special styling */
        .logout-section {{
            margin-top: auto;
            padding: 16px 8px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .logout-section .stButton > button {{
            background: rgba(220, 38, 38, 0.15);
            border-color: rgba(220, 38, 38, 0.3);
            color: #fca5a5;
        }}

        .logout-section .stButton > button:hover {{
            background: rgba(220, 38, 38, 0.25);
            border-color: rgba(220, 38, 38, 0.5);
            color: #ffffff;
        }}

        /* Hide default Streamlit sidebar elements */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: rgba(255, 255, 255, 0.85);
        }}

        [data-testid="stSidebar"] hr {{
            margin: 16px 8px;
            border-color: rgba(255, 255, 255, 0.1);
            opacity: 0.5;
        }}

        /* ===== Typography ===== */
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

        .page-subtitle {{
            font-size: 1.05rem;
            color: #64748b;
            font-weight: 400;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .subtitle-separator {{
            color: #cbd5e1;
            margin: 0 4px;
        }}

        /* ===== Cards & Containers ===== */
        .card {{
            background: #ffffff;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #e8edf5;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03), 0 1px 2px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease;
        }}

        .card:hover {{
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04), 0 2px 4px rgba(0, 0, 0, 0.03);
            border-color: #dce4f0;
        }}

        /* ===== Job Cards ===== */
        .job-card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 24px;
            border-radius: 10px;
            background: #ffffff;
            border: 1px solid #e8edf5;
            border-left: 4px solid {primary_color};
            margin-bottom: 12px;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .job-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            border-left-width: 5px;
        }}

        .job-card-content {{
            flex: 1;
        }}

        .job-title {{
            font-weight: 600;
            font-size: 1.05rem;
            color: #0f172a;
            margin-bottom: 6px;
            line-height: 1.3;
        }}

        .job-meta {{
            font-size: 0.875rem;
            color: #64748b;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .job-meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .job-stats {{
            text-align: right;
            min-width: 140px;
        }}

        .job-amount {{
            font-weight: 600;
            font-size: 1.15rem;
            color: #0f172a;
            margin-bottom: 4px;
        }}

        .job-margin {{
            font-size: 0.875rem;
            font-weight: 500;
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
        }}

        .margin-positive {{
            background: #ecfdf5;
            color: #059669;
        }}

        .margin-negative {{
            background: #fef2f2;
            color: #dc2626;
        }}

        /* ===== Metrics/KPI Cards ===== */
        [data-testid="stMetric"] {{
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e8edf5;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease;
        }}

        [data-testid="stMetric"]:hover {{
            border-color: {primary_color}40;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04);
        }}

        [data-testid="stMetric"] label {{
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: #64748b !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 2rem !important;
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

        .stButton > button[kind="primary"]:hover {{
            background: {primary_color}ee !important;
        }}

        .stButton > button[kind="secondary"] {{
            background: #ffffff !important;
            border-color: #e8edf5 !important;
            color: #334155 !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            border-color: #cbd5e1 !important;
            background: #f8fafc !important;
        }}

        /* ===== Section Headers ===== */
        .section-header {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e8edf5;
        }}

        /* ===== Quick Actions Panel ===== */
        .action-panel {{
            background: #ffffff;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #e8edf5;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        }}

        .action-panel-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 1rem;
        }}

        /* ===== Alert Card ===== */
        .alert-card {{
            margin-top: 20px;
            padding: 16px 18px;
            border-radius: 10px;
            border-left: 4px solid;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .alert-warning {{
            background: #fffbeb;
            border-color: #f59e0b;
            color: #92400e;
        }}

        .alert-success {{
            background: #ecfdf5;
            border-color: #10b981;
            color: #065f46;
        }}

        .alert-title {{
            font-weight: 600;
            margin-bottom: 4px;
        }}

        /* ===== Info Messages ===== */
        .stAlert {{
            border-radius: 10px;
            border-left-width: 4px;
            padding: 16px 20px;
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

        .empty-state-text {{
            color: #64748b;
            margin-bottom: 1.5rem;
        }}

        /* ===== Responsive Design ===== */
        @media (max-width: 768px) {{
            .block-container {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            
            .page-title {{
                font-size: 1.75rem;
            }}
            
            .job-card {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }}
            
            .job-stats {{
                text-align: left;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Enhanced Sidebar (Contractor-Friendly QuickBooks Style)
# --------------------------------------------------
def render_enhanced_sidebar(branding):
    """Render contractor-friendly QuickBooks-style sidebar navigation"""
    
    with st.sidebar:
        # Company Header
        company_name = branding.get("company_name", "Elite Wall Pro")
        user = st.session_state.get("user", {})
        user_name = user.get("name", "Admin User")
        user_role = user.get("role", "admin")
        
        st.markdown(f"""
        <div class="sidebar-header">
            <div class="sidebar-company-name">
                <div class="sidebar-company-icon">🏗️</div>
                <span>{company_name}</span>
            </div>
            <div class="sidebar-user-info">
                <div class="sidebar-user-name">{user_name}</div>
                <div class="sidebar-user-role">{user_role}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Navigation
        st.markdown('<div class="sidebar-nav-title">MAIN MENU</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-nav-section">', unsafe_allow_html=True)
        
        if st.button("🏠  Home", key="nav_home", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("📊  Dashboard", key="nav_dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
        
        if st.button("📋  Jobs", key="nav_jobs", use_container_width=True):
            st.switch_page("pages/2_Jobs.py")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<hr style="margin: 20px 8px; border-color: rgba(255, 255, 255, 0.1);">', unsafe_allow_html=True)
        
        # Transactions Section
        st.markdown('<div class="sidebar-nav-title">TRANSACTIONS</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-nav-section">', unsafe_allow_html=True)
        
        if st.button("💰  Cost Entry", key="trans_cost", use_container_width=True):
            st.switch_page("pages/3_Cost_Entry.py")
        
        if st.button("👥  Customers", key="trans_customers", use_container_width=True):
            st.switch_page("pages/4_Customers.py")
        
        if st.button("🏢  Vendors", key="trans_vendors", use_container_width=True):
            st.switch_page("pages/5_Vendors.py")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<hr style="margin: 20px 8px; border-color: rgba(255, 255, 255, 0.1);">', unsafe_allow_html=True)
        
        # Reports Section
        st.markdown('<div class="sidebar-nav-title">REPORTS</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-nav-section">', unsafe_allow_html=True)
        
        if st.button("📈  Reports", key="nav_reports", use_container_width=True):
            st.switch_page("pages/6_Reports.py")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Spacer for bottom logout
        st.markdown('<div style="flex-grow: 1; min-height: 40px;"></div>', unsafe_allow_html=True)
        
        # Logout Section
        st.markdown('<div class="logout-section">', unsafe_allow_html=True)
        if st.button("🚪  Logout", key="logout_btn", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.tenant = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Main Application
# --------------------------------------------------
def main():

    # Authentication (UNCHANGED)
    if not check_auth():
        render_login_page()
        return

    branding = get_branding()
    apply_global_css(branding["primary_color"])

    # Enhanced Sidebar
    render_enhanced_sidebar(branding)

    # --------------------------------------------------
    # Enhanced Header Section
    # --------------------------------------------------
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-title">Dashboard</div>
            <div class="page-subtitle">
                {branding["company_name"]}
                <span class="subtitle-separator">·</span>
                Job Costing Overview
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    api = st.session_state.api_client

    try:
        jobs = api.get_jobs() or []

        if not jobs:
            # Enhanced Empty State
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-state-icon">📋</div>
                    <div class="empty-state-title">No jobs yet</div>
                    <div class="empty-state-text">
                        Get started by creating your first job to begin tracking costs and revenue.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.button("➕ Create Your First Job", 
                         on_click=lambda: st.switch_page("pages/2_Jobs.py"),
                         type="primary",
                         use_container_width=True)
            return

        active_jobs = [j for j in jobs if j.get("status") == "active"]

        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        total_costs = sum(float(j.get("total_costs") or 0) for j in active_jobs)
        over_budget = len([j for j in active_jobs if float(j.get("variance") or 0) < 0])
        total_margin = ((total_contract - total_costs) / total_contract * 100) if total_contract else 0

        # --------------------------------------------------
        # Enhanced KPI Section
        # --------------------------------------------------
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Active Jobs", f"{len(active_jobs)}", delta=None)

        with c2:
            st.metric("Contract Value", f"${total_contract:,.0f}", delta=None)

        with c3:
            st.metric("Total Costs", f"${total_costs:,.0f}", 
                     delta=f"{total_margin:.1f}% margin")

        with c4:
            delta_text = f"-{over_budget} over budget" if over_budget > 0 else "All on track"
            st.metric("Risk Alerts", over_budget, 
                     delta=delta_text,
                     delta_color="inverse" if over_budget > 0 else "normal")

        st.write("")
        st.write("")

        # --------------------------------------------------
        # Enhanced Main Layout
        # --------------------------------------------------
        col_main, col_actions = st.columns([2.5, 1], gap="large")

        with col_main:
            st.markdown('<div class="section-header">Active Jobs</div>', unsafe_allow_html=True)

            # Show up to 8 jobs for better visibility
            display_jobs = active_jobs[:8] if len(active_jobs) > 8 else active_jobs
            
            for job in display_jobs:
                revenue = float(job.get("contract_amount") or 0)
                cost = float(job.get("total_costs") or 0)
                margin = ((revenue - cost) / revenue * 100) if revenue else 0
                
                status_color = "#dc2626" if margin < 0 else branding["primary_color"]
                margin_class = "margin-negative" if margin < 0 else "margin-positive"
                margin_icon = "⚠️" if margin < 0 else "✓"

                st.markdown(
                    f"""
                    <div class="job-card" style="border-left-color:{status_color}">
                        <div class="job-card-content">
                            <div class="job-title">{job.get("job_name", "Untitled Job")}</div>
                            <div class="job-meta">
                                <span class="job-meta-item">
                                    <strong>#{job.get("job_number", "N/A")}</strong>
                                </span>
                                <span>·</span>
                                <span class="job-meta-item">
                                    {job.get("customer_name", "No customer assigned")}
                                </span>
                            </div>
                        </div>
                        <div class="job-stats">
                            <div class="job-amount">${cost:,.0f}</div>
                            <div class="job-margin {margin_class}">
                                {margin_icon} {abs(margin):.1f}% margin
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Show "View All" button if there are more jobs
            if len(active_jobs) > 8:
                st.write("")
                col_center1, col_center2, col_center3 = st.columns([1, 1, 1])
                with col_center2:
                    st.button(
                        f"View All {len(active_jobs)} Jobs →",
                        use_container_width=True,
                        on_click=lambda: st.switch_page("pages/2_Jobs.py")
                    )

        with col_actions:
            st.markdown(
                """
                <div class="action-panel">
                    <div class="action-panel-title">Quick Actions</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.button("➕ New Job", 
                     use_container_width=True,
                     on_click=lambda: st.switch_page("pages/2_Jobs.py"),
                     type="primary")

            st.button("💰 Log Cost", 
                     use_container_width=True,
                     on_click=lambda: st.switch_page("pages/3_Cost_Entry.py"))

            st.button("📊 Reports", 
                     use_container_width=True,
                     on_click=lambda: st.switch_page("pages/6_Reports.py"))

            st.button("👥 Customers", 
                     use_container_width=True,
                     on_click=lambda: st.switch_page("pages/4_Customers.py"))

            # Enhanced Alert Card
            if over_budget > 0:
                st.markdown(
                    f"""
                    <div class="alert-card alert-warning">
                        <div class="alert-title">⚠️ Budget Alert</div>
                        <div>{over_budget} job{'s' if over_budget > 1 else ''} currently over budget. Review immediately.</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="alert-card alert-success">
                        <div class="alert-title">✓ All Clear</div>
                        <div>All jobs are on budget and tracking well.</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"⚠️ Failed to load dashboard data: {e}")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.button("🔄 Retry", on_click=st.rerun, use_container_width=True)


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    main()