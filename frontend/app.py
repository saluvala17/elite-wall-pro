"""
Elite Wall Pro - Executive Owner Dashboard
Comprehensive business intelligence for construction company owners
Performance optimized with smart caching and efficient queries
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from functools import lru_cache

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
    page_title="Elite Wall Pro - Executive Dashboard",
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

def get_branding():
    tenant = st.session_state.get("tenant") or {}
    if tenant:
        branding = tenant.get("branding", {})
        return {
            "primary_color": branding.get("primary_color", "#6366F1"),
            "company_name": branding.get("company_name", "Elite Wall Pro"),
            "logo_url": branding.get("logo_url"),
        }
    return {"primary_color": "#6366F1", "company_name": "Elite Wall Pro", "logo_url": None}


# --------------------------------------------------
# Executive Dashboard CSS
# --------------------------------------------------
def apply_executive_styles():
    st.markdown("""
        <style>
        /* Executive Dashboard Styling */
        .exec-header {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            padding: 2rem 3rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;
        }
        
        .exec-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.03em;
        }
        
        .exec-subtitle {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0F172A;
            margin: 2rem 0 1rem 0;
            padding-left: 1rem;
            border-left: 4px solid #6366F1;
        }
        
        /* KPI Cards - Executive Style */
        .kpi-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.3s ease;
            min-height: 140px;
        }
        
        .kpi-card:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        .kpi-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.75rem;
        }
        
        .kpi-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.1;
            margin-bottom: 0.5rem;
        }
        
        .kpi-subtitle {
            font-size: 0.875rem;
            color: #64748B;
        }
        
        .kpi-indicator-good {
            color: #059669;
            font-weight: 600;
        }
        
        .kpi-indicator-bad {
            color: #DC2626;
            font-weight: 600;
        }
        
        /* Status Badge */
        .status-excellent {
            background: #D1FAE5;
            color: #047857;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }
        
        .status-good {
            background: #FEF3C7;
            color: #B45309;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }
        
        .status-alert {
            background: #FEE2E2;
            color: #B91C1C;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
        }
        
        /* Chart Container */
        .chart-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }
        
        .chart-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 1rem;
        }
        
        /* Milestone Card */
        .milestone-card {
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .milestone-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }
        
        .milestone-name {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .milestone-date {
            font-size: 0.875rem;
            opacity: 0.9;
        }
        
        /* Equipment Card */
        .equipment-card {
            background: white;
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid #E2E8F0;
            margin-bottom: 0.75rem;
        }
        
        .equipment-name {
            font-size: 0.875rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.25rem;
        }
        
        .equipment-util {
            font-size: 1.25rem;
            font-weight: 700;
            color: #6366F1;
        }
        
        /* Progress Ring */
        .progress-ring-container {
            position: relative;
            width: 120px;
            height: 120px;
            margin: 0 auto;
        }
        
        .progress-ring-value {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.75rem;
            font-weight: 800;
            color: #0F172A;
        }
        </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# Performance-Optimized Helper Functions
# --------------------------------------------------

@st.cache_data(ttl=300)  # Cache for 5 minutes
def calculate_total_budget(job):
    """Calculate total budget - cached for performance"""
    return sum([
        float(job.get("budget_insurance", 0) or 0),
        float(job.get("budget_labor", 0) or 0),
        float(job.get("budget_stamps", 0) or 0),
        float(job.get("budget_material", 0) or 0),
        float(job.get("budget_subs_bond", 0) or 0),
        float(job.get("budget_equipment", 0) or 0)
    ])

def get_job_total_costs(api, job_id):
    """Get actual costs - optimized"""
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
# Executive KPI Components
# --------------------------------------------------

def render_revenue_profit_kpi(total_revenue, total_costs):
    """Financial Health - Revenue & Profit Margin"""
    profit = total_revenue - total_costs
    margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
    
    margin_status = "EXCELLENT" if margin >= 15 else "GOOD" if margin >= 10 else "ALERT"
    margin_class = "status-excellent" if margin >= 15 else "status-good" if margin >= 10 else "status-alert"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">Current Revenue & Profit</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
        <div class="kpi-subtitle">
            <span class="{margin_class}">{margin:.1f}% MARGIN</span>
            <span style="color: #059669; margin-left: 1rem;">+${profit:,.0f} Profit</span>
        </div>
    </div>
    """


def render_cash_flow_kpi(upcoming_payments):
    """Cash Flow - Upcoming Payments"""
    total_due = sum(p['amount'] for p in upcoming_payments)
    next_date = upcoming_payments[0]['date'] if upcoming_payments else "N/A"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">Cash Flow - Payments Due</div>
        <div class="kpi-value">${total_due:,.0f}</div>
        <div class="kpi-subtitle">
            Next payment: <strong>{next_date}</strong>
            <br><span style="color: #64748B;">{len(upcoming_payments)} upcoming payments</span>
        </div>
    </div>
    """


def render_active_jobs_kpi(progress_pct):
    """Active Jobs Progress"""
    status = "ON TRACK" if progress_pct >= 70 else "NEEDS ATTENTION" if progress_pct >= 50 else "BEHIND"
    color = "#059669" if progress_pct >= 70 else "#D97706" if progress_pct >= 50 else "#DC2626"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">Active Jobs Progress</div>
        <div class="kpi-value" style="color: {color};">{progress_pct:.0f}%</div>
        <div class="kpi-subtitle">
            Aggregate completion across all projects
            <br><span style="color: {color}; font-weight: 600;">{status}</span>
        </div>
    </div>
    """


def render_safety_kpi(incidents):
    """Safety Incidents - The Most Important Metric"""
    status = "ZERO INCIDENTS" if incidents == 0 else f"{incidents} INCIDENT{'S' if incidents != 1 else ''}"
    color = "#059669" if incidents == 0 else "#DC2626"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">Safety Record (30 Days)</div>
        <div class="kpi-value" style="color: {color};">{incidents}</div>
        <div class="kpi-subtitle">
            <span style="color: {color}; font-weight: 600;">{status}</span>
            <br><span style="color: #64748B;">Industry standard: &lt;0.5/month</span>
        </div>
    </div>
    """


def render_qc_pass_rate(pass_rate):
    """Quality Control Pass Rate"""
    status_class = "status-excellent" if pass_rate >= 95 else "status-good" if pass_rate >= 90 else "status-alert"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">Quality Control</div>
        <div class="kpi-value">{pass_rate:.1f}%</div>
        <div class="kpi-subtitle">
            <span class="{status_class}">PASS RATE</span>
            <br><span style="color: #64748B;">Workmanship quality checks</span>
        </div>
    </div>
    """


def render_client_satisfaction(rating):
    """Client Satisfaction Score"""
    stars = "⭐" * int(rating)
    status_class = "status-excellent" if rating >= 4.5 else "status-good" if rating >= 4.0 else "status-alert"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">Client Satisfaction</div>
        <div class="kpi-value">{rating:.1f}/5.0</div>
        <div class="kpi-subtitle">
            {stars}
            <br><span class="{status_class}">REPEAT BUSINESS DRIVER</span>
        </div>
    </div>
    """


def render_monthly_spending_chart():
    """Monthly Spending: Labor vs Materials vs Subcontractors"""
    # Sample data - replace with real API data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    fig = go.Figure()
    
    # Labor costs (smoother line)
    fig.add_trace(go.Scatter(
        x=dates,
        y=[50000 + i*1000 for i in range(30)],
        name='Labor',
        line=dict(color='#6366F1', width=3),
        fill='tonexty',
        fillcolor='rgba(99, 102, 241, 0.1)'
    ))
    
    # Materials (with spike mid-month)
    materials = [30000 + i*800 for i in range(30)]
    materials[15] = 65000  # Spike on day 15
    fig.add_trace(go.Scatter(
        x=dates,
        y=materials,
        name='Materials',
        line=dict(color='#059669', width=3),
        fill='tonexty',
        fillcolor='rgba(5, 150, 105, 0.1)'
    ))
    
    # Subcontractors
    fig.add_trace(go.Scatter(
        x=dates,
        y=[20000 + i*500 for i in range(30)],
        name='Subcontractors',
        line=dict(color='#D97706', width=3),
        fill='tonexty',
        fillcolor='rgba(217, 119, 6, 0.1)'
    ))
    
    fig.update_layout(
        title="",
        height=320,
        margin=dict(l=20, r=20, t=20, b=40),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#F1F5F9',
            title="",
            tickformat='%b %d'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F1F5F9',
            title="Daily Spending ($)",
            tickformat='$,.0f'
        )
    )
    
    return fig


def render_phase_breakdown_chart():
    """Phase Breakdown: Foundation, Framing, Finishing"""
    phases = ['Foundation', 'Framing', 'Finishing']
    values = [25, 45, 30]  # Sample percentages
    colors = ['#6366F1', '#10B981', '#F59E0B']
    
    fig = go.Figure(data=[go.Pie(
        labels=phases,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hole=0.4
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    return fig


def render_equipment_utilization():
    """Equipment Utilization Cards"""
    equipment = [
        {"name": "Tower Crane #1", "utilization": 92, "status": "Excellent"},
        {"name": "Scissor Lift #3", "utilization": 78, "status": "Good"},
        {"name": "Boom Lift #2", "utilization": 45, "status": "Underutilized"},
        {"name": "Concrete Mixer", "utilization": 88, "status": "Good"}
    ]
    
    html = ""
    for eq in equipment:
        color = "#059669" if eq["utilization"] >= 80 else "#D97706" if eq["utilization"] >= 60 else "#DC2626"
        html += f"""
        <div class="equipment-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="equipment-name">{eq['name']}</div>
                    <div style="font-size: 0.75rem; color: #64748B;">{eq['status']}</div>
                </div>
                <div class="equipment-util" style="color: {color};">{eq['utilization']}%</div>
            </div>
            <div style="margin-top: 0.5rem; height: 6px; background: #F1F5F9; border-radius: 3px; overflow: hidden;">
                <div style="width: {eq['utilization']}%; height: 100%; background: {color};"></div>
            </div>
        </div>
        """
    
    return html


# --------------------------------------------------
# Main Application
# --------------------------------------------------
def main():
    if not check_auth():
        render_login_page()
        return

    branding = get_branding()
    primary_color = branding.get("primary_color", "#6366F1")
    
    # Apply styles
    st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)
    apply_executive_styles()
    render_sidebar(branding)

    # ============================================
    # EXECUTIVE HEADER
    # ============================================
    st.markdown(f"""
    <div class="exec-header">
        <div class="exec-title">Executive Dashboard</div>
        <div class="exec-subtitle">{branding['company_name']} • Business Intelligence & KPIs</div>
    </div>
    """, unsafe_allow_html=True)

    api = st.session_state.api_client

    try:
        # Fetch data
        jobs = api.get_jobs() or []
        active_jobs = [j for j in jobs if j.get("status") == "active"]
        
        # Calculate financial metrics
        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        
        job_costs = {}
        for job in active_jobs:
            job_costs[job["id"]] = get_job_total_costs(api, job["id"])
        
        total_costs = sum(job_costs.values())
        
        # Sample data for upcoming payments
        upcoming_payments = [
            {"date": "Oct 22", "amount": 125000, "vendor": "ABC Supply"},
            {"date": "Oct 25", "amount": 48500, "vendor": "Labor Payroll"},
            {"date": "Oct 28", "amount": 32000, "vendor": "Equipment Rental"}
        ]
        
        # Sample operational data
        aggregate_progress = 78  # % completion across all jobs
        safety_incidents = 0  # Last 30 days
        qc_pass_rate = 95.2  # %
        client_satisfaction = 4.8  # out of 5
        total_employees = 85

        # ============================================
        # SECTION 1: FINANCIAL HEALTH
        # ============================================
        st.markdown('<div class="section-title">💰 Financial Health</div>', unsafe_allow_html=True)
        
        fin_col1, fin_col2, fin_col3 = st.columns(3)
        
        with fin_col1:
            st.markdown(render_revenue_profit_kpi(total_contract, total_costs), unsafe_allow_html=True)
        
        with fin_col2:
            st.markdown(render_cash_flow_kpi(upcoming_payments), unsafe_allow_html=True)
        
        with fin_col3:
            # Monthly spending chart
            st.markdown('<div class="chart-card"><div class="chart-title">Monthly Spending Breakdown</div></div>', unsafe_allow_html=True)
            st.plotly_chart(render_monthly_spending_chart(), use_container_width=True, config={'displayModeBar': False})

        # ============================================
        # SECTION 2: OPERATIONAL PROGRESS
        # ============================================
        st.markdown('<div class="section-title">📊 Operational Progress</div>', unsafe_allow_html=True)
        
        ops_col1, ops_col2, ops_col3 = st.columns(3)
        
        with ops_col1:
            st.markdown(render_active_jobs_kpi(aggregate_progress), unsafe_allow_html=True)
        
        with ops_col2:
            # Phase breakdown
            st.markdown('<div class="chart-card"><div class="chart-title">Phase Breakdown</div></div>', unsafe_allow_html=True)
            st.plotly_chart(render_phase_breakdown_chart(), use_container_width=True, config={'displayModeBar': False})
        
        with ops_col3:
            # Next big milestone
            st.markdown("""
            <div class="milestone-card">
                <div class="milestone-title">Next Big Milestone</div>
                <div class="milestone-name">Luxury Condo Tower</div>
                <div class="milestone-date">📅 Target: Nov 15, 2024</div>
                <div style="margin-top: 1rem; font-size: 0.875rem; opacity: 0.9;">
                    Foundation Complete: 95%<br>
                    Client: Metropolitan Developers
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ============================================
        # SECTION 3: RISK & QUALITY CONTROL
        # ============================================
        st.markdown('<div class="section-title">🛡️ Risk & Quality Control</div>', unsafe_allow_html=True)
        
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        
        with risk_col1:
            st.markdown(render_safety_kpi(safety_incidents), unsafe_allow_html=True)
        
        with risk_col2:
            st.markdown(render_qc_pass_rate(qc_pass_rate), unsafe_allow_html=True)
        
        with risk_col3:
            st.markdown(render_client_satisfaction(client_satisfaction), unsafe_allow_html=True)

        # ============================================
        # SECTION 4: RESOURCE MANAGEMENT
        # ============================================
        st.markdown('<div class="section-title">⚙️ Resource Management</div>', unsafe_allow_html=True)
        
        resource_col1, resource_col2 = st.columns([2, 1])
        
        with resource_col1:
            # Equipment utilization
            st.markdown('<div class="chart-card"><div class="chart-title">Equipment Utilization</div>', unsafe_allow_html=True)
            st.markdown(render_equipment_utilization(), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with resource_col2:
            # Total employees
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Workforce</div>
                <div class="kpi-value">{total_employees}</div>
                <div class="kpi-subtitle">
                    Active employees across all projects
                    <br><span style="color: #64748B;">Field: 68 | Office: 17</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.write("")
            
            # Additional capacity metric
            st.markdown("""
            <div class="kpi-card">
                <div class="kpi-label">Capacity for Growth</div>
                <div class="kpi-value">+35%</div>
                <div class="kpi-subtitle">
                    <span class="status-excellent">READY FOR NEW BIDS</span>
                    <br><span style="color: #64748B;">Can handle 3-4 more projects</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Error loading executive dashboard: {str(e)}")
        
        with st.expander("Debug Information"):
            import traceback
            st.code(traceback.format_exc())
        
        if st.button("🔄 Retry"):
            st.rerun()


if __name__ == "__main__":
    main()