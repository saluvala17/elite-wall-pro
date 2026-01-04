"""
Elite Wall Pro - Professional Dashboard
Final Enhancement: All UI refinements applied
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
# Enhanced Dashboard CSS - Final Version
# --------------------------------------------------
def apply_dashboard_styles():
    st.markdown(
        """
        <style>
        /* ===== Professional Spacing System ===== */
        
        /* Header Section */
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #E2E8F0;
        }
        
        .dashboard-title {
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 0.25rem;
            line-height: 1.2;
        }
        
        .dashboard-subtitle {
            font-size: 0.875rem;
            color: #64748B;
            line-height: 1.4;
        }
        
        /* Compact Action Buttons */
        .action-btn-small {
            padding: 0.5rem 0.875rem !important;
            font-size: 0.8125rem !important;
            height: 36px !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            border: 1px solid #E2E8F0 !important;
            background: white !important;
            color: #64748B !important;
            transition: all 0.2s ease !important;
        }
        
        .action-btn-small:hover {
            border-color: #CBD5E1 !important;
            background: #F8FAFC !important;
            color: #334155 !important;
        }
        
        /* Section Spacing - Tighter */
        .section-header {
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            margin-top: 1rem;
            margin-bottom: 0;
            letter-spacing: -0.01em;
        }
        
        /* KPI Cards - Consistent Height */
        [data-testid="stMetric"] {
            background: white;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            min-height: 115px;
            transition: all 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            border-color: #CBD5E1;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
        
        /* Custom Metric Card - Inline Layout */
        .custom-metric-card {
            background: white;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            min-height: 115px;
            transition: all 0.2s ease;
        }
        
        .custom-metric-card:hover {
            border-color: #CBD5E1;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }
        
        .metric-label-custom {
            font-size: 0.6875rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .metric-value-inline {
            display: flex;
            align-items: baseline;
            gap: 0.5rem;
        }
        
        .metric-main-value {
            font-size: 1.875rem;
            font-weight: 700;
            color: #0F172A;
        }
        
        .metric-sub-value {
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* Alert Badges - Compact */
        .alert-badge {
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.75rem;
        }
        
        .badge-danger {
            background: #FEE2E2;
            color: #DC2626;
        }
        
        .badge-warning {
            background: #FEF3C7;
            color: #D97706;
        }
        
        /* MODIFICATION 2: Job Cards - Ultra Compact Spacing */
        .job-card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.375rem;  /* CHANGED: Reduced from 0.5rem to 0.375rem */
            transition: all 0.2s ease;
            border-left-width: 3px;
        }
        
        .job-card:hover {
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            transform: translateY(-1px);
            border-color: #CBD5E1;
        }
        
        .job-card-over-budget {
            border-left-color: #DC2626;
        }
        
        .job-card-on-track {
            border-left-color: #10B981;
        }
        
        /* Search Bar Styling */
        .search-container {
            margin-bottom: 0.75rem;
        }
        
        /* Make search input align with header */
        [data-testid="stTextInput"] {
            margin-bottom: 0 !important;
        }
        
        [data-testid="stTextInput"] > div {
            margin-bottom: 0 !important;
        }
        
        .search-container input {
            border-radius: 8px !important;
            border: 1px solid #E2E8F0 !important;
            padding: 0.625rem 1rem !important;
            font-size: 0.875rem !important;
        }
        
        .search-container input:focus {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }
        
        /* Panel Sections - Professional Cards */
        .panel-section {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        
        .panel-title {
            font-size: 0.875rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Quick Action Buttons - Uniform Style */
        .stButton > button {
            width: 100% !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            padding: 0.625rem 1rem !important;
            margin-bottom: 0.5rem !important;
            transition: all 0.2s ease !important;
            height: 42px !important;
        }
        
        /* Primary Button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Secondary Buttons */
        .stButton > button:not([kind="primary"]) {
            background: white !important;
            border: 1px solid #E2E8F0 !important;
            color: #475569 !important;
        }
        
        .stButton > button:not([kind="primary"]):hover {
            background: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            color: #0F172A !important;
        }
        
        /* Chart Container */
        .chart-section {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 1.25rem;
        }
        
        .chart-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        
        /* Job Card Content Layout */
        .job-header {
            margin-bottom: 0.75rem;
        }
        
        .job-name {
            font-size: 1rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.25rem;
        }
        
        .job-meta {
            font-size: 0.8125rem;
            color: #64748B;
        }
        
        .budget-label {
            font-size: 0.6875rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }
        
        .budget-value {
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
        }
        
        /* Progress Bar */
        .progress-bar-container {
            width: 100%;
            height: 6px;
            background: #F1F5F9;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .progress-bar-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        
        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.625rem;
            border-radius: 4px;
            font-size: 0.6875rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        .badge-over {
            background: #FEE2E2;
            color: #DC2626;
        }
        
        .badge-success {
            background: #D1FAE5;
            color: #059669;
        }
        
        /* Reduced Spacing Between Sections */
        .section-divider {
            height: 1rem;
        }
        
        /* Compact Layout Utilities */
        .mb-tight {
            margin-bottom: 0.5rem;
        }
        
        .mb-normal {
            margin-bottom: 0.75rem;
        }
        
        .mb-loose {
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
    """Render a compact, professional job card"""
    
    # Calculate values
    progress_pct = (actual / budget * 100) if budget > 0 else 0
    margin = ((contract - actual) / contract * 100) if contract > 0 else 0
    card_class = "job-card-over-budget" if is_over_budget else "job-card-on-track"
    progress_color = "#DC2626" if is_over_budget else "#10B981"
    
    # Render card
    st.markdown(f'<div class="job-card {card_class}">', unsafe_allow_html=True)
    
    # Job header
    col1, col2, col3 = st.columns([2, 1.2, 1])
    
    with col1:
        st.markdown(f'<div class="job-name">{job.get("job_name", "Untitled Job")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="job-meta">#{job.get("job_number", "N/A")} · {job.get("customer_name", "No customer")}</div>', unsafe_allow_html=True)
        
        st.write("")
        st.markdown('<div class="budget-label">BUDGET</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="budget-value">${budget:,.0f}</div>', unsafe_allow_html=True)
        
        # Progress bar
        st.markdown(f"""
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: {min(progress_pct, 100):.1f}%; background: {progress_color};"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="budget-label">ACTUAL</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 1.5rem; font-weight: 700; color: #0F172A;">${actual:,.0f}</div>', unsafe_allow_html=True)
        
        # Status badge
        if is_over_budget:
            st.markdown('<div class="status-badge badge-over">⚠️ Over Budget</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-badge badge-success">✓ {margin:.1f}% margin</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="font-size: 0.6875rem; color: #94A3B8; margin-top: 0.5rem;">Last cost: 3 days ago</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="budget-label">ACTUAL</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 1.25rem; font-weight: 700; color: #0F172A;">${actual:,.0f}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    # MODIFICATION 2: Removed <hr> separator - spacing handled by margin-bottom


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
    apply_dashboard_styles()

    # Render sidebar
    render_sidebar(branding)

    # ============================================
    # HEADER - Professional Layout
    # ============================================
    header_left, header_right = st.columns([3, 1])
    
    with header_left:
        st.markdown("""
        <div class="dashboard-title">Dashboard</div>
        <div class="dashboard-subtitle">Elite Wall Pro • Job Costing Overview</div>
        """, unsafe_allow_html=True)
    
    with header_right:
        btn1, btn2 = st.columns(2)
        with btn1:
            st.markdown('<button class="action-btn-small">📥 Export</button>', unsafe_allow_html=True)
        with btn2:
            st.markdown('<button class="action-btn-small">📅 Date Range</button>', unsafe_allow_html=True)

    # Small divider
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

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
                if 0 <= margin < 10 and actual > 0:
                    near_threshold_jobs.append(job)

        # ============================================
        # FINANCIAL SNAPSHOT - Compact Section
        # ============================================
        st.markdown('<div class="section-header">Financial Snapshot</div>', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric("ACTIVE JOBS", len(active_jobs))
        
        with m2:
            st.metric("CONTRACT VALUE", f"${total_contract:,.0f}")
        
        # MODIFICATION 3: Custom metric with inline margin
        with m3:
            st.markdown(f"""
            <div class="custom-metric-card">
                <div class="metric-label-custom">TOTAL COSTS</div>
                <div class="metric-value-inline">
                    <div class="metric-main-value">${total_costs:,.0f}</div>
                    <div class="metric-sub-value" style="color: #059669;">↑ {total_margin:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # MODIFICATION 4: Custom metric with inline over budget
        with m4:
            over_budget_count = len(over_budget_jobs)
            sub_color = '#DC2626' if over_budget_count > 0 else '#059669'
            sub_text = f'↓ {over_budget_count} over' if over_budget_count > 0 else '✓ All on track'
            
            st.markdown(f"""
            <div class="custom-metric-card">
                <div class="metric-label-custom">RISK ALERTS</div>
                <div class="metric-value-inline">
                    <div class="metric-main-value">{over_budget_count}</div>
                    <div class="metric-sub-value" style="color: {sub_color};">{sub_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Alert Badges - Compact
        if len(over_budget_jobs) > 0 or len(near_threshold_jobs) > 0:
            badge_html = ""
            if len(over_budget_jobs) > 0:
                badge_html += f'<span class="alert-badge badge-danger">🔴 {len(over_budget_jobs)} Job{"s" if len(over_budget_jobs) > 1 else ""} Over Budget</span>'
            if len(near_threshold_jobs) > 0:
                badge_html += f'<span class="alert-badge badge-warning">⚠️ {len(near_threshold_jobs)} Job{"s" if len(near_threshold_jobs) > 1 else ""} Near Threshold</span>'
            
            st.markdown(badge_html, unsafe_allow_html=True)

        # Reduced spacing
        st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

        # ============================================
        # MAIN LAYOUT - Jobs + Sidebar Panels
        # ============================================
        col_jobs, col_sidebar = st.columns([2.5, 1], gap="large")

        with col_jobs:
            # MODIFICATION 1: Search beside Active Jobs header
            header_col, search_col = st.columns([1, 1.5])
            
            with header_col:
                st.markdown('<div class="section-header">Active Jobs</div>', unsafe_allow_html=True)
            
            with search_col:
                search_query = st.text_input("🔍 Search jobs...", 
                                            placeholder="Search by job name, number, or customer", 
                                            label_visibility="collapsed", 
                                            key="job_search")
            
            # Small spacing
            st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)
            
            # Filter jobs if search query exists
            filtered_jobs = active_jobs
            if search_query:
                search_lower = search_query.lower()
                filtered_jobs = [
                    j for j in active_jobs 
                    if search_lower in j.get("job_name", "").lower() 
                    or search_lower in j.get("job_number", "").lower()
                    or search_lower in j.get("customer_name", "").lower()
                ]
            
            # Render job cards with ultra-tight spacing
            if filtered_jobs:
                for job in filtered_jobs:
                    job_id = job["id"]
                    budget = calculate_total_budget(job)
                    actual = job_costs.get(job_id, 0)
                    contract = float(job.get("contract_amount") or 0)
                    is_over_budget = actual > budget if budget > 0 else False
                    
                    render_job_card(job, budget, actual, contract, is_over_budget)
            else:
                st.info(f"No jobs found matching '{search_query}'")

        with col_sidebar:
            # ============================================
            # QUICK ACTIONS - Consolidated Panel
            # ============================================
            st.markdown("""
            <div class="panel-section">
                <div class="panel-title">Quick Actions</div>
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
            
            # ============================================
            # BUDGET VS ACTUAL - Separate Panel
            # ============================================
            st.markdown("""
            <div class="chart-section">
                <div class="chart-title">Budget vs Actual (Top 5)</div>
            </div>
            """, unsafe_allow_html=True)
            
            top_5 = sorted(active_jobs, key=lambda x: float(x.get("contract_amount") or 0), reverse=True)[:5]
            
            if top_5:
                labels = [j.get("job_number", "")[:10] for j in top_5]
                budgets = [calculate_total_budget(j) for j in top_5]
                actuals = [job_costs.get(j["id"], 0) for j in top_5]
                
                fig = go.Figure(data=[
                    go.Bar(name='Budget', x=labels, y=budgets, marker_color='#CBD5E1', width=0.35),
                    go.Bar(name='Actual', x=labels, y=actuals, marker_color='#10B981', width=0.35)
                ])
                
                fig.update_layout(
                    barmode='group',
                    height=260,
                    margin=dict(l=10, r=10, t=10, b=40),
                    showlegend=False,
                    plot_bgcolor='white',
                    xaxis=dict(
                        showgrid=False, 
                        showline=True, 
                        linecolor='#E2E8F0', 
                        tickfont=dict(size=10, color='#64748B'),
                        tickangle=-45
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
        
        with st.expander("Debug Information"):
            import traceback
            st.code(traceback.format_exc())
        
        if st.button("🔄 Retry"):
            st.rerun()


if __name__ == "__main__":
    main()