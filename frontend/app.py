"""
Elite Wall Pro - Production Dashboard
Pure Streamlit Components - Maximum Reliability
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
from components.shared_styles import get_professional_css

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Elite Wall Pro - Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit defaults
st.markdown("""
    <style>
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session State
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
# Helper Functions
# --------------------------------------------------
def get_branding():
    """Get tenant branding"""
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


def calculate_total_budget(job):
    """Calculate total budget from all budget fields"""
    try:
        return sum([
            float(job.get("budget_insurance", 0) or 0),
            float(job.get("budget_labor", 0) or 0),
            float(job.get("budget_stamps", 0) or 0),
            float(job.get("budget_material", 0) or 0),
            float(job.get("budget_subs_bond", 0) or 0),
            float(job.get("budget_equipment", 0) or 0)
        ])
    except Exception as e:
        st.error(f"Error calculating budget: {e}")
        return 0


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
    except Exception as e:
        # Silent fail - return 0 if API call fails
        pass
    return 0


def apply_custom_css():
    """Apply minimal custom CSS for polish"""
    st.markdown("""
    <style>
    /* Clean typography */
    h1, h2, h3 { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    
    /* Alert badges */
    .alert-badge {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0.5rem 1rem 0;
    }
    
    .badge-danger {
        background: #FEE2E2;
        color: #DC2626;
    }
    
    .badge-warning {
        background: #FEF3C7;
        color: #D97706;
    }
    
    /* Job cards */
    .job-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .job-card-over-budget {
        border-left: 4px solid #DC2626;
    }
    
    .job-card-on-track {
        border-left: 4px solid #10B981;
    }
    </style>
    """, unsafe_allow_html=True)


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
    
    # Apply styles
    st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)
    apply_custom_css()

    # Render sidebar
    render_sidebar(branding)

    # Header
    col_title, col_actions = st.columns([3, 1])
    
    with col_title:
        st.title("Dashboard")
        st.caption(f"{branding['company_name']} • Job Costing Overview")
    
    with col_actions:
        btn1, btn2 = st.columns(2)
        with btn1:
            st.button("📥 Export", key="export_btn", use_container_width=True)
        with btn2:
            st.button("📅 Date Range", key="date_btn", use_container_width=True)

    st.write("")

    api = st.session_state.api_client

    try:
        # Fetch jobs
        jobs = api.get_jobs() or []

        if not jobs:
            st.info("📋 No jobs yet. Create your first job to get started.")
            if st.button("➕ Create First Job", type="primary"):
                st.switch_page("pages/2_Jobs.py")
            return

        # Filter active jobs only
        active_jobs = [j for j in jobs if j.get("status") == "active"]
        
        if not active_jobs:
            st.warning("No active jobs found. All jobs may be completed or inactive.")
            return
        
        # Calculate all costs upfront
        job_costs = {}
        job_budgets = {}
        
        for job in active_jobs:
            job_id = job["id"]
            job_costs[job_id] = get_job_total_costs(api, job_id)
            job_budgets[job_id] = calculate_total_budget(job)
        
        # Calculate financial metrics
        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        total_costs = sum(job_costs.values())
        total_margin = ((total_contract - total_costs) / total_contract * 100) if total_contract > 0 else 0
        
        # Identify problem jobs
        over_budget_jobs = []
        near_threshold_jobs = []
        
        for job in active_jobs:
            job_id = job["id"]
            budget = job_budgets[job_id]
            actual = job_costs[job_id]
            contract = float(job.get("contract_amount") or 0)
            
            # Over budget check
            if budget > 0 and actual > budget:
                over_budget_jobs.append(job)
            
            # Near threshold check (margin < 10%)
            if contract > 0:
                margin = ((contract - actual) / contract * 100)
                if 0 <= margin < 10 and actual > 0:
                    near_threshold_jobs.append(job)

        # ============================================
        # FINANCIAL SNAPSHOT
        # ============================================
        st.subheader("Financial Snapshot")
        
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

        st.write("")

        # ============================================
        # MAIN LAYOUT: JOBS + QUICK ACTIONS
        # ============================================
        col_jobs, col_qa = st.columns([2.5, 1], gap="large")

        with col_jobs:
            st.subheader("Active Jobs")
            
            # Display each job as a card
            for job in active_jobs:
                job_id = job["id"]
                job_name = job.get("job_name", "Untitled Job")
                job_number = job.get("job_number", "N/A")
                customer_name = job.get("customer_name", "No customer")
                
                budget = job_budgets[job_id]
                actual = job_costs[job_id]
                contract = float(job.get("contract_amount") or 0)
                
                # Calculate progress and status
                progress = (actual / budget) if budget > 0 else 0
                is_over_budget = actual > budget if budget > 0 else False
                
                if contract > 0 and actual > 0:
                    margin = ((contract - actual) / contract * 100)
                else:
                    margin = 0
                
                # Card container
                card_class = "job-card-over-budget" if is_over_budget else "job-card-on-track"
                
                with st.container():
                    st.markdown(f'<div class="job-card {card_class}">', unsafe_allow_html=True)
                    
                    # Job header
                    st.markdown(f"**{job_name}**")
                    st.caption(f"#{job_number} · {customer_name}")
                    
                    # Three columns for details
                    detail_col1, detail_col2, detail_col3 = st.columns([2, 1.5, 1])
                    
                    with detail_col1:
                        st.caption("BUDGET")
                        st.markdown(f"**${budget:,.0f}**")
                        
                        # Progress bar
                        if budget > 0:
                            progress_pct = min(progress * 100, 100)
                            progress_color = "#DC2626" if is_over_budget else "#10B981"
                            st.progress(progress, text=f"{progress_pct:.0f}% used")
                    
                    with detail_col2:
                        st.caption("ACTUAL")
                        st.markdown(f"### ${actual:,.0f}")
                        
                        # Status badge
                        if is_over_budget:
                            st.error("⚠️ Over Budget", icon="🚨")
                        elif margin > 0:
                            st.success(f"✓ {margin:.1f}% margin", icon="✅")
                        
                        st.caption("Last cost: 3 days ago")
                    
                    with detail_col3:
                        st.caption("CONTRACT")
                        st.markdown(f"**${contract:,.0f}**")
                        
                        if contract > 0:
                            completion = (actual / contract * 100) if contract > 0 else 0
                            st.caption(f"{completion:.0f}% complete")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.write("")

        with col_qa:
            # Quick Actions Panel
            st.subheader("Quick Actions")
            
            if st.button("➕ New Job", type="primary", use_container_width=True, key="qa_new"):
                st.switch_page("pages/2_Jobs.py")
            
            if st.button("💵 Log Cost", use_container_width=True, key="qa_cost"):
                st.switch_page("pages/3_Cost_Entry.py")
            
            if st.button("📄 Upload Invoice", use_container_width=True, key="qa_invoice"):
                st.switch_page("pages/3_Cost_Entry.py")
            
            if st.button("📊 View Reports", use_container_width=True, key="qa_reports"):
                st.switch_page("pages/6_Reports.py")
            
            st.write("")
            st.write("")
            
            # Budget vs Actual Chart
            st.caption("BUDGET VS ACTUAL (TOP 5)")
            
            # Get top 5 jobs by contract value
            top_5 = sorted(active_jobs, key=lambda x: float(x.get("contract_amount") or 0), reverse=True)[:5]
            
            if top_5:
                labels = []
                budgets = []
                actuals = []
                
                for job in top_5:
                    labels.append(job.get("job_number", "")[:10])
                    budgets.append(job_budgets[job["id"]])
                    actuals.append(job_costs[job["id"]])
                
                fig = go.Figure(data=[
                    go.Bar(
                        name='Budget',
                        x=labels,
                        y=budgets,
                        marker_color='#CBD5E1',
                        width=0.35
                    ),
                    go.Bar(
                        name='Actual',
                        x=labels,
                        y=actuals,
                        marker_color='#10B981',
                        width=0.35
                    )
                ])
                
                fig.update_layout(
                    barmode='group',
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=40),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10)
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
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
                        tickfont=dict(size=10, color='#64748B'),
                        tickformat='$,.0f'
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error(f"⚠️ Error loading dashboard: {str(e)}")
        
        # Debug info (remove in production)
        with st.expander("Debug Information"):
            st.code(f"""
Error: {str(e)}

Debug Info:
- Jobs fetched: {len(jobs) if 'jobs' in locals() else 'N/A'}
- Active jobs: {len(active_jobs) if 'active_jobs' in locals() else 'N/A'}
- API client: {st.session_state.api_client}
            """)
        
        if st.button("🔄 Retry"):
            st.rerun()


if __name__ == "__main__":
    main()