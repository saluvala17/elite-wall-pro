"""
Elite Wall Pro - Streamlit Frontend
Modern Purple Theme with Bold Sidebar Navigation
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
# Session State Initialization
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
            "primary_color": branding.get("primary_color", "#7C3AED"),
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url"),
        }
    return {
        "primary_color": "#7C3AED",
        "company_name": "Elite Wall Pro",
        "logo_url": None,
    }


# --------------------------------------------------
# Enhanced Global UI Styling (Purple/Violet Theme)
# --------------------------------------------------
def apply_global_css(primary_color: str):
    st.markdown(
        f"""
        <style>
        /* ===== Global Foundation ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #f5f3ff;
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

        /* ===== Enhanced Sidebar Styling (Purple Theme) ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #5B21B6 0%, #7C3AED 50%, #8B5CF6 100%);
            border-right: none;
            box-shadow: 4px 0 20px rgba(124, 58, 237, 0.15);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: transparent;
            padding-top: 1.5rem;
        }}

        /* Sidebar Logo - Top Left */
        .sidebar-logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 16px;
            margin: 0 0 0 0;
        }}

        .sidebar-logo-icon {{
            background: rgba(255, 255, 255, 0.2);
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            flex-shrink: 0;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}

        .sidebar-logo-text {{
            color: #ffffff;
            font-size: 1.2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }}

        /* Override Streamlit's button styling in sidebar - Unified Menu */
        [data-testid="stSidebar"] .stButton {{
            margin-bottom: 8px;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #ffffff;
            text-align: left;
            padding: 14px 18px;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 700;
            transition: all 0.2s ease;
            height: auto;
            min-height: 48px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.18);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateX(3px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}

        [data-testid="stSidebar"] .stButton > button:active {{
            background: rgba(255, 255, 255, 0.25);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.35);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }}

        /* Logout button special styling */
        .logout-section {{
            margin-top: auto;
            padding: 16px 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
        }}

        .logout-section .stButton > button {{
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.3);
            color: #FCA5A5;
            font-weight: 700;
        }}

        .logout-section .stButton > button:hover {{
            background: rgba(239, 68, 68, 0.25);
            border-color: rgba(239, 68, 68, 0.5);
            color: #ffffff;
        }}

        /* Hide default Streamlit sidebar elements */
        [data-testid="stSidebar"] hr {{
            margin: 20px 12px;
            border-color: rgba(255, 255, 255, 0.15);
            opacity: 0.6;
        }}

        /* ===== Typography ===== */
        .page-header {{
            margin-bottom: 2.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 2px solid #e9d5ff;
        }}

        .page-title {{
            font-size: 2.25rem;
            font-weight: 800;
            color: #5B21B6;
            margin-bottom: 0.5rem;
            letter-spacing: -0.03em;
            line-height: 1.2;
        }}

        .page-subtitle {{
            font-size: 1.05rem;
            color: #9333EA;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .subtitle-separator {{
            color: #c4b5fd;
            margin: 0 4px;
        }}

        /* ===== Cards & Containers ===== */
        .card {{
            background: #ffffff;
            padding: 24px;
            border-radius: 14px;
            border: 1px solid #ede9fe;
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08), 0 1px 3px rgba(124, 58, 237, 0.05);
            transition: all 0.3s ease;
        }}

        .card:hover {{
            box-shadow: 0 8px 16px rgba(124, 58, 237, 0.12), 0 4px 8px rgba(124, 58, 237, 0.08);
            border-color: #ddd6fe;
            transform: translateY(-2px);
        }}

        /* ===== Job Cards ===== */
        .job-card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 22px 26px;
            border-radius: 12px;
            background: #ffffff;
            border: 1px solid #ede9fe;
            border-left: 5px solid {primary_color};
            margin-bottom: 14px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .job-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.15);
            border-left-width: 6px;
        }}

        .job-card-content {{
            flex: 1;
        }}

        .job-title {{
            font-weight: 700;
            font-size: 1.1rem;
            color: #1e1b4b;
            margin-bottom: 7px;
            line-height: 1.3;
        }}

        .job-meta {{
            font-size: 0.9rem;
            color: #7c3aed;
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 500;
        }}

        .job-meta-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .job-stats {{
            text-align: right;
            min-width: 150px;
        }}

        .job-amount {{
            font-weight: 700;
            font-size: 1.2rem;
            color: #1e1b4b;
            margin-bottom: 5px;
        }}

        .job-margin {{
            font-size: 0.9rem;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 8px;
            display: inline-block;
        }}

        .margin-positive {{
            background: #dcfce7;
            color: #15803d;
        }}

        .margin-negative {{
            background: #fee2e2;
            color: #dc2626;
        }}

        /* ===== Metrics/KPI Cards ===== */
        [data-testid="stMetric"] {{
            background: #ffffff;
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #ede9fe;
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08);
            transition: all 0.3s ease;
        }}

        [data-testid="stMetric"]:hover {{
            border-color: {primary_color}60;
            box-shadow: 0 8px 16px rgba(124, 58, 237, 0.15);
            transform: translateY(-2px);
        }}

        [data-testid="stMetric"] label {{
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #7c3aed !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #5B21B6 !important;
        }}

        /* ===== Buttons ===== */
        .stButton > button {{
            border-radius: 10px;
            height: 46px;
            font-weight: 700;
            font-size: 0.95rem;
            border: 2px solid transparent;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(124, 58, 237, 0.15);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(124, 58, 237, 0.25);
        }}

        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%) !important;
            border-color: #7C3AED !important;
            color: #ffffff !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #6D28D9 0%, #7C3AED 100%) !important;
        }}

        .stButton > button[kind="secondary"] {{
            background: #ffffff !important;
            border-color: #e9d5ff !important;
            color: #7C3AED !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            border-color: #c4b5fd !important;
            background: #faf5ff !important;
        }}

        /* ===== Section Headers ===== */
        .section-header {{
            font-size: 1.35rem;
            font-weight: 700;
            color: #5B21B6;
            margin-bottom: 1.2rem;
            padding-bottom: 0.8rem;
            border-bottom: 2px solid #e9d5ff;
        }}

        /* ===== Quick Actions Panel ===== */
        .action-panel {{
            background: linear-gradient(135deg, #faf5ff 0%, #ffffff 100%);
            padding: 26px;
            border-radius: 14px;
            border: 1px solid #e9d5ff;
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.08);
        }}

        .action-panel-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #5B21B6;
            margin-bottom: 1.2rem;
        }}

        /* ===== Alert Card ===== */
        .alert-card {{
            margin-top: 20px;
            padding: 18px 20px;
            border-radius: 12px;
            border-left: 5px solid;
            font-size: 0.92rem;
            line-height: 1.6;
        }}

        .alert-warning {{
            background: #fef3c7;
            border-color: #f59e0b;
            color: #92400e;
        }}

        .alert-success {{
            background: #d1fae5;
            border-color: #10b981;
            color: #065f46;
        }}

        .alert-title {{
            font-weight: 700;
            margin-bottom: 5px;
            font-size: 1rem;
        }}

        /* ===== Info Messages ===== */
        .stAlert {{
            border-radius: 12px;
            border-left-width: 5px;
            padding: 18px 22px;
        }}

        /* ===== Empty State ===== */
        .empty-state {{
            text-align: center;
            padding: 70px 30px;
            background: linear-gradient(135deg, #faf5ff 0%, #ffffff 100%);
            border-radius: 16px;
            border: 2px dashed #ddd6fe;
        }}

        .empty-state-icon {{
            font-size: 3.5rem;
            margin-bottom: 1.2rem;
            opacity: 0.6;
        }}

        .empty-state-title {{
            font-size: 1.4rem;
            font-weight: 700;
            color: #5B21B6;
            margin-bottom: 0.6rem;
        }}

        .empty-state-text {{
            color: #7c3aed;
            margin-bottom: 1.8rem;
            font-size: 1.05rem;
        }}

        /* ===== Responsive Design ===== */
        @media (max-width: 768px) {{
            .block-container {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            
            .page-title {{
                font-size: 1.85rem;
            }}
            
            .job-card {{
                flex-direction: column;
                align-items: flex-start;
                gap: 14px;
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
# Enhanced Sidebar (Purple Theme - Professional SaaS Style)
# --------------------------------------------------
def render_enhanced_sidebar(branding):
    """Render purple-themed sidebar with clean, unified navigation"""
    
    with st.sidebar:
        # Company Logo - Top Left
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        st.markdown(f"""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🏗️</div>
            <span class="sidebar-logo-text">{company_name}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 28px 0;"></div>', unsafe_allow_html=True)
        
        # Unified Navigation Menu (No Section Headers)
        if st.button("🏠  Dashboard", key="nav_home", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("📊  Analytics", key="nav_dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
        
        if st.button("📋  Jobs", key="nav_jobs", use_container_width=True):
            st.switch_page("pages/2_Jobs.py")
        
        if st.button("💰  Cost Entry", key="trans_cost", use_container_width=True):
            st.switch_page("pages/3_Cost_Entry.py")
        
        if st.button("👥  Customers", key="trans_customers", use_container_width=True):
            st.switch_page("pages/4_Customers.py")
        
        if st.button("🏢  Vendors", key="trans_vendors", use_container_width=True):
            st.switch_page("pages/5_Vendors.py")
        
        if st.button("📈  Reports", key="nav_reports", use_container_width=True):
            st.switch_page("pages/6_Reports.py")
        
        # Spacer
        st.markdown('<div style="flex-grow: 1; min-height: 50px;"></div>', unsafe_allow_html=True)
        
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

    # Authentication
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

            # Show up to 8 jobs
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
            
            # Show "View All" button if more jobs
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