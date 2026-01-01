"""
Elite Wall Pro - Streamlit Frontend
Professional QuickBooks-Style UI
(UI-only enhancements, no functional changes)
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
            "primary_color": branding.get("primary_color", "#2CA01C"),  # QuickBooks Green
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url"),
        }
    return {
        "primary_color": "#2CA01C",
        "company_name": "Elite Wall Pro",
        "logo_url": None,
    }


# --------------------------------------------------
# Global UI Styling (QuickBooks Inspired)
# --------------------------------------------------
def apply_global_css(primary_color: str):
    st.markdown(
        f"""
        <style>
        html, body {{
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f8fafc;
        }}

        .page-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0.25rem;
        }}

        .page-subtitle {{
            font-size: 1rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }}

        .card {{
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }}

        .job-card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px;
            border-radius: 10px;
            border-left: 5px solid {primary_color};
            background: #ffffff;
            border: 1px solid #e5e7eb;
            margin-bottom: 12px;
        }}

        .job-title {{
            font-weight: 600;
            font-size: 1rem;
            color: #111827;
        }}

        .job-meta {{
            font-size: 0.85rem;
            color: #6b7280;
        }}

        .metric-card div[data-testid="stMetric"] {{
            background: #ffffff;
            padding: 18px;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
        }}

        .stButton > button {{
            border-radius: 8px;
            height: 44px;
            font-weight: 600;
        }}

        [data-testid="stSidebar"] {{
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


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

    # Sidebar (UNCHANGED FUNCTIONALLY)
    render_sidebar(branding)

    # --------------------------------------------------
    # Header Section
    # --------------------------------------------------
    st.markdown(
        f"""
        <div>
            <div class="page-title">Dashboard</div>
            <div class="page-subtitle">
                {branding["company_name"]} · Job Costing Overview
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    api = st.session_state.api_client

    try:
        jobs = api.get_jobs() or []

        if not jobs:
            st.info("No jobs available yet. Create your first job to begin tracking costs.")
            st.button("➕ Create Job", on_click=lambda: st.switch_page("pages/2_Jobs.py"))
            return

        active_jobs = [j for j in jobs if j.get("status") == "active"]

        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        total_costs = sum(float(j.get("total_costs") or 0) for j in active_jobs)
        over_budget = len([j for j in active_jobs if float(j.get("variance") or 0) < 0])

        # --------------------------------------------------
        # KPI Section
        # --------------------------------------------------
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Active Jobs", len(active_jobs))

        with c2:
            st.metric("Contract Value", f"${total_contract:,.0f}")

        with c3:
            st.metric("Total Costs", f"${total_costs:,.0f}")

        with c4:
            st.metric("Risk Alerts", over_budget)

        st.write("")

        # --------------------------------------------------
        # Main Layout
        # --------------------------------------------------
        col_main, col_actions = st.columns([3, 1], gap="large")

        with col_main:
            st.markdown("### Active Jobs")

            for job in active_jobs[:6]:
                revenue = float(job.get("contract_amount") or 0)
                cost = float(job.get("total_costs") or 0)
                margin = ((revenue - cost) / revenue * 100) if revenue else 0
                status_color = "#dc2626" if margin < 0 else branding["primary_color"]

                st.markdown(
                    f"""
                    <div class="job-card" style="border-left-color:{status_color}">
                        <div>
                            <div class="job-title">{job.get("job_name")}</div>
                            <div class="job-meta">
                                {job.get("job_number")} · {job.get("customer_name", "N/A")}
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-weight:600">${cost:,.0f}</div>
                            <div style="font-size:0.85rem;color:{status_color}">
                                {margin:.1f}% margin
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_actions:
            st.markdown("### Quick Actions")

            st.button("➕ New Job", use_container_width=True,
                      on_click=lambda: st.switch_page("pages/2_Jobs.py"),
                      type="primary")

            st.button("💰 Log Cost", use_container_width=True,
                      on_click=lambda: st.switch_page("pages/3_Cost_Entry.py"))

            st.button("📊 Reports", use_container_width=True,
                      on_click=lambda: st.switch_page("pages/6_Reports.py"))

            st.button("👥 Customers", use_container_width=True,
                      on_click=lambda: st.switch_page("pages/4_Customers.py"))

            st.markdown(
                f"""
                <div class="card" style="margin-top:20px;background:#f0fdf4;border-color:#bbf7d0">
                    <strong>Heads up</strong><br/>
                    {over_budget} job(s) currently over budget.
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Failed to load dashboard data: {e}")
        st.button("🔄 Retry", on_click=st.rerun)


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    main()
