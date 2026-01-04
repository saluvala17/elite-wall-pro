"""
Elite Wall Pro - Streamlit Frontend
Professional SaaS Color Palette (Inspired by Notion, Linear, Slack)
Muted, Sophisticated Colors for Better UX
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
            "primary_color": branding.get("primary_color", "#6366F1"),  # Professional Indigo
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url"),
        }
    return {
        "primary_color": "#6366F1",  # Indigo-500
        "company_name": "Elite Wall Pro",
        "logo_url": None,
    }


# --------------------------------------------------
# Professional SaaS Color Palette (Research-Based)
# --------------------------------------------------
def apply_global_css(primary_color: str):
    st.markdown(
        f"""
        <style>
        /* ===== Professional Color Palette ===== */
        :root {{
            /* Primary Colors - Sophisticated Indigo (Like Linear/Notion) */
            --primary-600: #4F46E5;
            --primary-500: #6366F1;
            --primary-400: #818CF8;
            
            /* Sidebar Colors - Deep Navy/Slate (Professional) */
            --sidebar-bg-start: #1E293B;
            --sidebar-bg-mid: #334155;
            --sidebar-bg-end: #475569;
            
            /* Neutral Grays - Clean & Modern */
            --gray-50: #F8FAFC;
            --gray-100: #F1F5F9;
            --gray-200: #E2E8F0;
            --gray-300: #CBD5E1;
            --gray-600: #475569;
            --gray-700: #334155;
            --gray-800: #1E293B;
            --gray-900: #0F172A;
            
            /* Semantic Colors */
            --success: #10B981;
            --success-light: #D1FAE5;
            --warning: #F59E0B;
            --warning-light: #FEF3C7;
            --danger: #EF4444;
            --danger-light: #FEE2E2;
        }}
        
        /* ===== Global Foundation ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: var(--gray-50);
            color: var(--gray-900);
        }}

        /* Remove default Streamlit padding */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            max-width: 1400px !important;
        }}

        /* ===== Professional Sidebar (Slate/Navy) ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--sidebar-bg-start) 0%, var(--sidebar-bg-mid) 50%, var(--sidebar-bg-end) 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: transparent;
            padding-top: 0.5rem;
        }}

        /* Sidebar Logo - Absolute Top Corner */
        .sidebar-logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 16px 12px 16px;
            margin: 0;
        }}

        .sidebar-logo-icon {{
            background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%);
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }}

        .sidebar-logo-text {{
            color: #ffffff;
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        /* Sidebar Navigation Buttons */
        [data-testid="stSidebar"] .stButton {{
            margin-bottom: 6px;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: rgba(255, 255, 255, 0.9);
            text-align: left;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            transition: all 0.2s ease;
            height: auto;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 10px;
        }}

        /* White arrow for navigation */
        [data-testid="stSidebar"] .stButton > button::after {{
            content: '';
            margin-left: auto;
            width: 0;
            height: 0;
            border-top: 4px solid transparent;
            border-bottom: 4px solid transparent;
            border-left: 5px solid rgba(255, 255, 255, 0.4);
            transition: all 0.2s ease;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateX(2px);
        }}

        [data-testid="stSidebar"] .stButton > button:hover::after {{
            border-left-color: rgba(255, 255, 255, 0.9);
        }}

        /* Logout button */
        .logout-section {{
            margin-top: auto;
            padding: 16px 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .logout-section .stButton > button {{
            background: rgba(239, 68, 68, 0.12);
            border-color: rgba(239, 68, 68, 0.2);
            color: #FCA5A5;
        }}

        .logout-section .stButton > button::after {{
            display: none;
        }}

        .logout-section .stButton > button:hover {{
            background: rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.3);
        }}

        /* ===== Main Content Typography ===== */
        .page-header {{
            margin-bottom: 2.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--gray-200);
        }}

        .page-title {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--gray-900);
            margin-bottom: 0.5rem;
            letter-spacing: -0.03em;
        }}

        .page-subtitle {{
            font-size: 1rem;
            color: var(--gray-600);
            font-weight: 500;
        }}

        .subtitle-separator {{
            color: var(--gray-400);
            margin: 0 6px;
        }}

        /* ===== Cards & Containers ===== */
        .card {{
            background: #ffffff;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid var(--gray-200);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }}

        .card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            border-color: var(--gray-300);
        }}

        /* ===== Job Cards ===== */
        .job-card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 24px;
            border-radius: 10px;
            background: #ffffff;
            border: 1px solid var(--gray-200);
            border-left: 4px solid {primary_color};
            margin-bottom: 12px;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .job-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            border-left-width: 5px;
        }}

        .job-title {{
            font-weight: 600;
            font-size: 1.05rem;
            color: var(--gray-900);
            margin-bottom: 6px;
        }}

        .job-meta {{
            font-size: 0.875rem;
            color: var(--gray-600);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .job-amount {{
            font-weight: 700;
            font-size: 1.15rem;
            color: var(--gray-900);
            margin-bottom: 4px;
        }}

        .job-margin {{
            font-size: 0.875rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
        }}

        .margin-positive {{
            background: var(--success-light);
            color: var(--success);
        }}

        .margin-negative {{
            background: var(--danger-light);
            color: var(--danger);
        }}

        /* ===== Metrics/KPI Cards ===== */
        [data-testid="stMetric"] {{
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid var(--gray-200);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }}

        [data-testid="stMetric"]:hover {{
            border-color: {primary_color}40;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
        }}

        [data-testid="stMetric"] label {{
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            color: var(--gray-600) !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--gray-900) !important;
        }}

        /* ===== Buttons ===== */
        .stButton > button {{
            border-radius: 8px;
            height: 44px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        }}

        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%) !important;
            border: none !important;
            color: #ffffff !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
        }}

        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
        }}

        .stButton > button[kind="secondary"] {{
            background: #ffffff !important;
            border: 1px solid var(--gray-300) !important;
            color: var(--gray-700) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background: var(--gray-50) !important;
            border-color: var(--gray-400) !important;
        }}

        /* ===== Section Headers ===== */
        .section-header {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--gray-900);
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--gray-200);
        }}

        /* ===== Alert Cards ===== */
        .alert-card {{
            margin-top: 24px;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid;
            font-size: 0.95rem;
            line-height: 1.6;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }}

        .alert-warning {{
            background: var(--warning-light);
            border-color: var(--warning);
            color: #92400e;
        }}

        .alert-success {{
            background: var(--success-light);
            border-color: var(--success);
            color: #065f46;
        }}

        .alert-title {{
            font-weight: 700;
            margin-bottom: 4px;
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

        .empty-state-text {{
            color: var(--gray-600);
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
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Professional Sidebar
# --------------------------------------------------
def render_enhanced_sidebar(branding):
    """Render professional SaaS sidebar with muted colors"""
    
    with st.sidebar:
        # Company Logo
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        st.markdown(f"""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🏗️</div>
            <span class="sidebar-logo-text">{company_name}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
        
        # Unified Navigation
        if st.button("🏠  Dashboard", key="nav_home", use_container_width=True):
            st.switch_page("app.py")
        
        # if st.button("📊  Analytics", key="nav_dashboard", use_container_width=True):
        #     st.switch_page("pages/1_Dashboard.py")
        
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
        
        # Logout
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

    # Sidebar
    render_enhanced_sidebar(branding)

    # Header
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

        # KPI Section
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Active Jobs", f"{len(active_jobs)}")

        with c2:
            st.metric("Contract Value", f"${total_contract:,.0f}")

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

        # Full-Width Active Jobs Section
        st.markdown('<div class="section-header">Active Jobs</div>', unsafe_allow_html=True)

        display_jobs = active_jobs[:8] if len(active_jobs) > 8 else active_jobs
        
        for job in display_jobs:
            revenue = float(job.get("contract_amount") or 0)
            cost = float(job.get("total_costs") or 0)
            margin = ((revenue - cost) / revenue * 100) if revenue else 0
            
            status_color = "#EF4444" if margin < 0 else branding["primary_color"]
            margin_class = "margin-negative" if margin < 0 else "margin-positive"
            margin_icon = "⚠️" if margin < 0 else "✓"

            st.markdown(
                f"""
                <div class="job-card" style="border-left-color:{status_color}">
                    <div class="job-card-content">
                        <div class="job-title">{job.get("job_name", "Untitled Job")}</div>
                        <div class="job-meta">
                            <strong>#{job.get("job_number", "N/A")}</strong>
                            <span>·</span>
                            <span>{job.get("customer_name", "No customer assigned")}</span>
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
        
        if len(active_jobs) > 8:
            st.write("")
            col_center1, col_center2, col_center3 = st.columns([1, 1, 1])
            with col_center2:
                st.button(
                    f"View All {len(active_jobs)} Jobs →",
                    use_container_width=True,
                    on_click=lambda: st.switch_page("pages/2_Jobs.py")
                )

        st.write("")
        st.write("")

        # Quick Actions - Horizontal Layout at Bottom
        st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)
        
        # Create 4-column horizontal layout for action buttons
        action_col1, action_col2, action_col3, action_col4 = st.columns(4, gap="medium")
        
        with action_col1:
            if st.button("➕ New Job", 
                        use_container_width=True,
                        type="primary",
                        key="qa_new_job"):
                st.switch_page("pages/2_Jobs.py")

        with action_col2:
            if st.button("💰 Log Cost", 
                        use_container_width=True,
                        key="qa_log_cost"):
                st.switch_page("pages/3_Cost_Entry.py")

        with action_col3:
            if st.button("📊 Reports", 
                        use_container_width=True,
                        key="qa_reports"):
                st.switch_page("pages/6_Reports.py")

        with action_col4:
            if st.button("👥 Customers", 
                        use_container_width=True,
                        key="qa_customers"):
                st.switch_page("pages/4_Customers.py")

        # Alert Card - Full Width at Bottom
        st.write("")
        if over_budget > 0:
            st.markdown(
                f"""
                <div class="alert-card alert-warning">
                    <div class="alert-title">⚠️ Budget Alert</div>
                    <div>{over_budget} job{'s' if over_budget > 1 else ''} currently over budget.</div>
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