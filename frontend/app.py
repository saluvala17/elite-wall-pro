"""
Elite Wall Pro - Professional Dashboard
Matching Design Mockup - Production Ready
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

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
# Professional Dashboard CSS - Matching Design
# --------------------------------------------------
def apply_dashboard_css(primary_color: str):
    st.markdown(
        f"""
        <style>
        /* ===== Typography & Colors ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }}
        
        .block-container {{
            padding: 1.5rem 2.5rem !important;
            max-width: 1600px !important;
        }}
        
        /* ===== Header Section ===== */
        .dashboard-header {{
            margin-bottom: 2rem;
        }}
        
        .dashboard-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.25rem;
        }}
        
        .dashboard-subtitle {{
            font-size: 0.875rem;
            color: #64748B;
            font-weight: 400;
        }}
        
        /* ===== Section Titles ===== */
        .section-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            margin: 2rem 0 1rem 0;
        }}
        
        /* ===== KPI Metric Cards ===== */
        [data-testid="stMetric"] {{
            background: white;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            min-height: 120px;
        }}
        
        [data-testid="stMetric"] label {{
            font-size: 0.6875rem !important;
            font-weight: 600 !important;
            color: #64748B !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 0.5rem !important;
        }}
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 1.875rem !important;
            font-weight: 700 !important;
            color: #0F172A !important;
            line-height: 1.2 !important;
        }}
        
        [data-testid="stMetric"] [data-testid="stMetricDelta"] {{
            font-size: 0.75rem !important;
            font-weight: 600 !important;
        }}
        
        /* ===== Alert Badges ===== */
        .alert-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.8125rem;
            font-weight: 600;
            margin-right: 0.75rem;
            margin-bottom: 1.5rem;
        }}
        
        .badge-danger {{
            background: #FEE2E2;
            color: #DC2626;
        }}
        
        .badge-warning {{
            background: #FEF3C7;
            color: #D97706;
        }}
        
        /* ===== Job Cards ===== */
        .job-card {{
            background: white;
            border: 1px solid #E2E8F0;
            border-left: 4px solid;
            border-radius: 8px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }}
        
        .job-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transform: translateY(-1px);
        }}
        
        .job-card-grid {{
            display: grid;
            grid-template-columns: 2fr 1.2fr 1fr;
            gap: 2rem;
            align-items: center;
        }}
        
        .job-info {{
            min-width: 0;
        }}
        
        .job-name {{
            font-size: 0.9375rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.375rem;
        }}
        
        .job-meta {{
            font-size: 0.8125rem;
            color: #64748B;
            font-weight: 500;
        }}
        
        .job-budget-section {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .budget-label {{
            font-size: 0.6875rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .budget-value {{
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
        }}
        
        .progress-container {{
            width: 100%;
            margin-top: 0.375rem;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 6px;
            background: #F1F5F9;
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.4s ease;
        }}
        
        .job-actual-section {{
            text-align: right;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            align-items: flex-end;
        }}
        
        .actual-label {{
            font-size: 0.6875rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .actual-value {{
            font-size: 1.25rem;
            font-weight: 700;
            color: #0F172A;
        }}
        
        .status-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.6875rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .badge-success {{
            background: #D1FAE5;
            color: #059669;
        }}
        
        .badge-over {{
            background: #FEE2E2;
            color: #DC2626;
        }}
        
        .last-cost-text {{
            font-size: 0.6875rem;
            color: #94A3B8;
            font-weight: 500;
        }}
        
        /* ===== Quick Actions Panel ===== */
        .quick-actions {{
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.5rem;
        }}
        
        .qa-title {{
            font-size: 1rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 1rem;
        }}
        
        .stButton > button {{
            width: 100% !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            padding: 0.625rem 1rem !important;
            margin-bottom: 0.5rem !important;
            border: 1px solid #E2E8F0 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }}
        
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
            color: white !important;
            border: none !important;
        }}
        
        /* ===== Chart Container ===== */
        .chart-box {{
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem;
            margin-top: 1rem;
        }}
        
        .chart-title {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: #64748B;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* ===== Header Buttons ===== */
        .header-btn {{
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Helper: Calculate Total Budget
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


# --------------------------------------------------
# Helper: Get Total Costs from API
# --------------------------------------------------
def get_job_total_costs(api, job_id):
    """Get actual total costs for a job from weekly_costs"""
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


# --------------------------------------------------
# Main Application
# --------------------------------------------------
def main():
    # Authentication
    if not check_auth():
        render_login_page()
        return

    branding = get_branding()
    apply_dashboard_css(branding["primary_color"])

    # Render sidebar
    render_sidebar(branding)

    # Header Section
    col_title, col_actions = st.columns([3, 1])
    
    with col_title:
        st.markdown(f"""
        <div class="dashboard-header">
            <div class="dashboard-title">Dashboard</div>
            <div class="dashboard-subtitle">{branding["company_name"]} • Job Costing Overview</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_actions:
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 0.2])
        with btn_col1:
            st.button("📥 Export", key="export_btn", use_container_width=True)
        with btn_col2:
            st.button("📅 Date Range", key="date_btn", use_container_width=True)

    api = st.session_state.api_client

    try:
        # Fetch all jobs
        jobs = api.get_jobs() or []

        if not jobs:
            st.info("📋 No jobs yet. Create your first job to get started.")
            return

        # Filter active jobs
        active_jobs = [j for j in jobs if j.get("status") == "active"]
        
        # Calculate metrics from REAL data
        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        
        # Get REAL total costs from API for each job
        job_costs = {}
        for job in active_jobs:
            job_costs[job["id"]] = get_job_total_costs(api, job["id"])
        
        total_costs = sum(job_costs.values())
        total_margin = ((total_contract - total_costs) / total_contract * 100) if total_contract > 0 else 0
        
        # Calculate over budget jobs
        over_budget_jobs = []
        near_threshold_jobs = []
        
        for job in active_jobs:
            job_id = job["id"]
            budget = calculate_total_budget(job)
            actual = job_costs.get(job_id, 0)
            contract = float(job.get("contract_amount") or 0)
            
            # Over budget check
            if budget > 0 and actual > budget:
                over_budget_jobs.append(job)
            
            # Near threshold check (margin < 10%)
            if contract > 0:
                margin = ((contract - actual) / contract * 100)
                if 0 <= margin < 10:
                    near_threshold_jobs.append(job)

        # Financial Snapshot Section
        st.markdown('<div class="section-title">Financial Snapshot</div>', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4, gap="medium")
        
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
            badges_html = ""
            if len(over_budget_jobs) > 0:
                badges_html += f'<span class="alert-badge badge-danger">🔴 {len(over_budget_jobs)} Job{"s" if len(over_budget_jobs) > 1 else ""} Over Budget</span>'
            if len(near_threshold_jobs) > 0:
                badges_html += f'<span class="alert-badge badge-warning">⚠️ {len(near_threshold_jobs)} Job{"s" if len(near_threshold_jobs) > 1 else ""} Near Margin Threshold</span>'
            
            st.markdown(badges_html, unsafe_allow_html=True)

        # Main Layout: Jobs + Quick Actions
        col_jobs, col_actions_panel = st.columns([2.5, 1], gap="large")

        with col_jobs:
            st.markdown('<div class="section-title">Active Jobs</div>', unsafe_allow_html=True)
            
            # Display all active jobs
            for job in active_jobs:
                job_id = job["id"]
                job_name = job.get("job_name", "Untitled Job")
                job_number = job.get("job_number", "N/A")
                customer_name = job.get("customer_name", "No customer")
                
                # Calculate financials
                budget = calculate_total_budget(job)
                actual = job_costs.get(job_id, 0)
                contract = float(job.get("contract_amount") or 0)
                
                # Calculate progress and margin
                progress_pct = (actual / budget * 100) if budget > 0 else 0
                is_over_budget = actual > budget
                
                if contract > 0:
                    margin = ((contract - actual) / contract * 100)
                else:
                    margin = 0
                
                # Colors
                border_color = "#DC2626" if is_over_budget else "#10B981"
                progress_color = "#DC2626" if is_over_budget else "#10B981"
                
                # Job Card HTML
                st.markdown(f"""
                <div class="job-card" style="border-left-color: {border_color}">
                    <div class="job-card-grid">
                        <div class="job-info">
                            <div class="job-name">{job_name}</div>
                            <div class="job-meta">#{job_number} · {customer_name}</div>
                            <div class="job-budget-section">
                                <div class="budget-label">Budget</div>
                                <div class="budget-value">${budget:,.0f}</div>
                                <div class="progress-container">
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: {min(progress_pct, 100):.1f}%; background-color: {progress_color};"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="job-actual-section" style="text-align: center;">
                            <div class="budget-label" style="text-align: center;">Actual</div>
                            <div class="actual-value" style="font-size: 1.5rem;">$ {actual:,.0f}</div>
                            <div class="status-badge {'badge-over' if is_over_budget else 'badge-success'}">
                                {'⚠️ Over Budget' if is_over_budget else f'✓ {margin:.1f}% margin'}
                            </div>
                            <div class="last-cost-text">Last cost: 3 days ago</div>
                        </div>
                        
                        <div class="job-actual-section">
                            <div class="actual-label">Actual</div>
                            <div class="actual-value">$ {actual:,.0f}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_actions_panel:
            # Quick Actions Panel
            st.markdown("""
            <div class="quick-actions">
                <div class="qa-title">Quick Actions</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➕ New Job", type="primary", use_container_width=True, key="qa_new_job"):
                st.switch_page("pages/2_Jobs.py")
            
            if st.button("💵 Log Cost", use_container_width=True, key="qa_log_cost"):
                st.switch_page("pages/3_Cost_Entry.py")
            
            if st.button("📄 Upload Invoice", use_container_width=True, key="qa_upload"):
                st.switch_page("pages/3_Cost_Entry.py")
            
            if st.button("📊 View Reports", use_container_width=True, key="qa_reports"):
                st.switch_page("pages/6_Reports.py")
            
            # Budget vs Actual Chart (Top 5)
            st.markdown("""
            <div class="chart-box">
                <div class="chart-title">Budget vs Actual (Top 5)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Get top 5 jobs by contract value
            top_5_jobs = sorted(active_jobs, key=lambda x: float(x.get("contract_amount") or 0), reverse=True)[:5]
            
            if top_5_jobs:
                job_labels = []
                budget_values = []
                actual_values = []
                
                for job in top_5_jobs:
                    job_labels.append(job.get("job_number", "")[:8])
                    budget_values.append(calculate_total_budget(job))
                    actual_values.append(job_costs.get(job["id"], 0))
                
                fig = go.Figure(data=[
                    go.Bar(
                        name='Budget',
                        x=job_labels,
                        y=budget_values,
                        marker_color='#CBD5E1',
                        width=0.35
                    ),
                    go.Bar(
                        name='Actual',
                        x=job_labels,
                        y=actual_values,
                        marker_color='#10B981',
                        width=0.35
                    )
                ])
                
                fig.update_layout(
                    barmode='group',
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=40),
                    showlegend=False,
                    plot_bgcolor='white',
                    xaxis=dict(
                        showgrid=False,
                        showline=True,
                        linecolor='#E2E8F0',
                        tickfont=dict(size=10, color='#64748B')
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#F1F5F9',
                        showline=False,
                        tickfont=dict(size=10, color='#64748B')
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error(f"⚠️ Error loading dashboard: {str(e)}")
        import traceback
        st.code(traceback.format_exc())


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    main()