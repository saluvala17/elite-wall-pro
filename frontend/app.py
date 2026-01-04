"""
Elite Wall Pro - Professional Dashboard
Fixed: Proper rendering, matching sidebar colors
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go

# Add components to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from api_client import APIClient
from components.auth import render_login_page, check_auth
from components.sidebar import render_sidebar
from components.shared_styles import get_professional_css

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
# Hide Streamlit Defaults
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
    tenant = st.session_state.get("tenant") or {}
    if tenant:
        branding = tenant.get("branding", {})
        return {
            "primary_color": branding.get("primary_color", "#6366F1"),
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url"),
        }
    return {
        "primary_color": "#6366F1",
        "company_name": "Elite Wall Pro",
        "logo_url": None,
    }


# --------------------------------------------------
# Dashboard-Specific CSS
# --------------------------------------------------
def apply_dashboard_styles():
    st.markdown(
        """
        <style>
        /* Dashboard specific overrides */
        
        /* Header */
        .dashboard-title {
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.25rem;
        }
        
        .dashboard-subtitle {
            font-size: 0.875rem;
            color: #64748B;
            margin-bottom: 2rem;
        }
        
        /* Section Titles */
        h3 {
            font-size: 1.125rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* KPI Cards - Match design exactly */
        [data-testid="stMetric"] {
            background: white;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            min-height: 110px;
        }
        
        [data-testid="stMetric"] label {
            font-size: 0.6875rem !important;
            font-weight: 600 !important;
            color: #64748B !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.875rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
        }
        
        /* Alert Badges */
        .alert-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.8125rem;
            font-weight: 600;
            margin-right: 0.75rem;
            margin-bottom: 1.5rem;
        }
        
        .badge-danger {
            background: #FEE2E2;
            color: #DC2626;
        }
        
        .badge-warning {
            background: #FEF3C7;
            color: #D97706;
        }
        
        /* Job Card Container */
        .job-card-container {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }
        
        .job-card-container:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transform: translateY(-1px);
        }
        
        /* Quick Actions Panel */
        .qa-panel {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .qa-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 1rem;
        }
        
        /* Quick Action Buttons */
        div[data-testid="column"] .stButton > button {
            width: 100% !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            padding: 0.625rem 1rem !important;
            margin-bottom: 0.5rem !important;
            transition: all 0.2s ease !important;
        }
        
        /* Primary button (New Job) */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
            color: white !important;
            border: none !important;
        }
        
        /* Chart Container */
        .chart-container {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem;
        }
        
        .chart-title {
            font-size: 0.8125rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def calculate_total_budget(job):
    """Calculate total budget from all budget fields"""
    return sum([
        float(job.get("budget_insurance", 0) or 0),
        float(job.get("budget_labor", 0) or 0),
        float(job.get("budget_stamps", 0) or 0),
        float(job.get("budget_material", 0) or 0),
        float(job.get("budget_subs_bond", 0) or 0),
        float(job.get("budget_equipment", 0) or 0)
    ])


def get_job_total_costs(api, job_id):
    """Get actual total costs for a job"""
    try:
        totals = api.get_cost_totals(job_id)
        if totals and totals.get("actual"):
            actual = totals["actual"]
            return sum([
                float(actual.get("insurance", 0) or 0),
                float(actual.get("labor", 0) or 0),
                float(actual.get("stamps", 0) or 0),
                float(actual.get("material", 0) or 0),
                float(actual.get("subs_bond", 0) or 0),
                float(actual.get("equipment", 0) or 0)
            ])
    except:
        pass
    return 0


def render_job_card(job, budget, actual, contract, is_over_budget):
    """Render a single job card using Streamlit columns"""
    
    # Calculate values
    progress_pct = (actual / budget * 100) if budget > 0 else 0
    margin = ((contract - actual) / contract * 100) if contract > 0 else 0
    border_color = "#DC2626" if is_over_budget else "#10B981"
    
    # Create card with border
    st.markdown(f"""
    <div style="border-left: 4px solid {border_color}; padding-left: 0;">
    """, unsafe_allow_html=True)
    
    # Create 3-column layout
    col1, col2, col3 = st.columns([2, 1.2, 1])
    
    with col1:
        st.markdown(f"**{job.get('job_name', 'Untitled Job')}**")
        st.caption(f"#{job.get('job_number', 'N/A')} · {job.get('customer_name', 'No customer')}")
        
        st.write("")
        st.caption("BUDGET")
        st.markdown(f"**${budget:,.0f}**")
        
        # Progress bar
        progress_color = "#DC2626" if is_over_budget else "#10B981"
        st.markdown(f"""
        <div style="width: 100%; background: #F1F5F9; height: 6px; border-radius: 3px; margin-top: 0.5rem;">
            <div style="width: {min(progress_pct, 100):.1f}%; background: {progress_color}; height: 100%; border-radius: 3px;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.caption("ACTUAL")
        st.markdown(f"### $ {actual:,.0f}")
        
        if is_over_budget:
            st.markdown("""
            <div style="background: #FEE2E2; color: #DC2626; padding: 0.25rem 0.75rem; 
                        border-radius: 4px; font-size: 0.6875rem; font-weight: 600; 
                        display: inline-block; margin-top: 0.5rem;">
                ⚠️ Over Budget
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #D1FAE5; color: #059669; padding: 0.25rem 0.75rem; 
                        border-radius: 4px; font-size: 0.6875rem; font-weight: 600; 
                        display: inline-block; margin-top: 0.5rem;">
                ✓ {margin:.1f}% margin
            </div>
            """, unsafe_allow_html=True)
        
        st.caption("Last cost: 3 days ago")
    
    with col3:
        st.caption("ACTUAL")
        st.markdown(f"### $ {actual:,.0f}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.75rem 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)


# --------------------------------------------------
# Main Application
# --------------------------------------------------
def main():
    # Authentication
    if not check_auth():
        render_login_page()
        return

    branding = get_branding()
    primary_color = branding.get("primary_color", "#6366F1")
    
    # Apply shared styles first
    st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)
    
    # Apply dashboard-specific styles
    apply_dashboard_styles()

    # Render sidebar
    render_sidebar(branding)

    # Header
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        st.markdown(f"""
        <div class="dashboard-title">Dashboard</div>
        <div class="dashboard-subtitle">{branding["company_name"]} • Job Costing Overview</div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        btn1, btn2 = st.columns(2)
        with btn1:
            st.button("📥 Export", key="export_btn", use_container_width=True)
        with btn2:
            st.button("📅 Date Range", key="date_btn", use_container_width=True)

    api = st.session_state.api_client

    try:
        # Fetch jobs
        jobs = api.get_jobs() or []

        if not jobs:
            st.info("📋 No jobs yet. Create your first job to get started.")
            return

        active_jobs = [j for j in jobs if j.get("status") == "active"]
        
        # Calculate metrics
        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        
        job_costs = {}
        for job in active_jobs:
            job_costs[job["id"]] = get_job_total_costs(api, job["id"])
        
        total_costs = sum(job_costs.values())
        total_margin = ((total_contract - total_costs) / total_contract * 100) if total_contract > 0 else 0
        
        # Calculate alerts
        over_budget_jobs = []
        near_threshold_jobs = []
        
        for job in active_jobs:
            job_id = job["id"]
            budget = calculate_total_budget(job)
            actual = job_costs.get(job_id, 0)
            contract = float(job.get("contract_amount") or 0)
            
            if budget > 0 and actual > budget:
                over_budget_jobs.append(job)
            
            if contract > 0:
                margin = ((contract - actual) / contract * 100)
                if 0 <= margin < 10:
                    near_threshold_jobs.append(job)

        # Financial Snapshot
        st.markdown("### Financial Snapshot")
        
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric("ACTIVE JOBS", len(active_jobs))
        
        with m2:
            st.metric("CONTRACT VALUE", f"${total_contract:,.0f}")
        
        with m3:
            st.metric("TOTAL COSTS", f"${total_costs:,.0f}", 
                     delta=f"{total_margin:.1f}% margin")
        
        with m4:
            st.metric("RISK ALERTS", len(over_budget_jobs), 
                     delta=f"{len(over_budget_jobs)} over budget" if len(over_budget_jobs) > 0 else "All on track",
                     delta_color="inverse" if len(over_budget_jobs) > 0 else "normal")

        # Alert Badges
        if len(over_budget_jobs) > 0 or len(near_threshold_jobs) > 0:
            badge_html = ""
            if len(over_budget_jobs) > 0:
                badge_html += f'<span class="alert-badge badge-danger">🔴 {len(over_budget_jobs)} Job{"s" if len(over_budget_jobs) > 1 else ""} Over Budget</span>'
            if len(near_threshold_jobs) > 0:
                badge_html += f'<span class="alert-badge badge-warning">⚠️ {len(near_threshold_jobs)} Job{"s" if len(near_threshold_jobs) > 1 else ""} Near Margin Threshold</span>'
            
            st.markdown(badge_html, unsafe_allow_html=True)

        # Main Layout
        col_jobs, col_qa = st.columns([2.5, 1], gap="large")

        with col_jobs:
            st.markdown("### Active Jobs")
            
            st.markdown('<div class="job-card-container">', unsafe_allow_html=True)
            
            for job in active_jobs:
                job_id = job["id"]
                budget = calculate_total_budget(job)
                actual = job_costs.get(job_id, 0)
                contract = float(job.get("contract_amount") or 0)
                is_over_budget = actual > budget if budget > 0 else False
                
                render_job_card(job, budget, actual, contract, is_over_budget)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with col_qa:
            # Quick Actions
            st.markdown("""
            <div class="qa-panel">
                <div class="qa-title">Quick Actions</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➕ New Job", type="primary", use_container_width=True, key="qa_new"):
                st.switch_page("pages/2_Jobs.py")
            
            if st.button("💵 Log Cost", use_container_width=True, key="qa_cost"):
                st.switch_page("pages/3_Cost_Entry.py")
            
            if st.button("📄 Upload Invoice", use_container_width=True, key="qa_invoice"):
                st.switch_page("pages/3_Cost_Entry.py")
            
            if st.button("📊 View Reports", use_container_width=True, key="qa_reports"):
                st.switch_page("pages/6_Reports.py")
            
            # Chart
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Budget vs Actual (Top 5)</div>
            </div>
            """, unsafe_allow_html=True)
            
            top_5 = sorted(active_jobs, key=lambda x: float(x.get("contract_amount") or 0), reverse=True)[:5]
            
            if top_5:
                labels = [j.get("job_number", "")[:8] for j in top_5]
                budgets = [calculate_total_budget(j) for j in top_5]
                actuals = [job_costs.get(j["id"], 0) for j in top_5]
                
                fig = go.Figure(data=[
                    go.Bar(name='Budget', x=labels, y=budgets, marker_color='#CBD5E1', width=0.35),
                    go.Bar(name='Actual', x=labels, y=actuals, marker_color='#10B981', width=0.35)
                ])
                
                fig.update_layout(
                    barmode='group',
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=40),
                    showlegend=False,
                    plot_bgcolor='white',
                    xaxis=dict(showgrid=False, showline=True, linecolor='#E2E8F0', 
                              tickfont=dict(size=10, color='#64748B')),
                    yaxis=dict(showgrid=True, gridcolor='#F1F5F9', showline=False, 
                              tickfont=dict(size=10, color='#64748B'))
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error(f"⚠️ Error loading dashboard: {str(e)}")


if __name__ == "__main__":
    main()