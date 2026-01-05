"""
Elite Wall Pro - Executive Owner Dashboard (FIXED)
Proper alignment + Real Supabase data integration
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from api_client import APIClient
from components.auth import render_login_page, check_auth
from components.sidebar import render_sidebar
from components.shared_styles import get_professional_css

st.set_page_config(
    page_title="Elite Wall Pro - Executive Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Session State
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


# ============================================
# FIXED: Professional Executive CSS
# ============================================
def apply_executive_styles():
    st.markdown("""
        <style>
        /* Executive Header - Full Width */
        .exec-header {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            padding: 2.5rem 3rem;
            border-radius: 16px;
            margin: -1rem 0 2.5rem 0;
            color: white;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }
        
        .exec-title {
            font-size: 2.75rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.03em;
        }
        
        .exec-subtitle {
            font-size: 1.125rem;
            opacity: 0.9;
            font-weight: 500;
        }
        
        /* FIXED: Section Divider - Properly Aligned */
        .section-divider {
            display: flex;
            align-items: center;
            margin: 2.5rem 0 1.5rem 0;
            gap: 1rem;
        }
        
        .section-icon {
            font-size: 1.75rem;
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }
        
        .section-title-text {
            font-size: 1.5rem;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: -0.02em;
        }
        
        /* KPI Cards */
        .kpi-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .kpi-card:hover {
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }
        
        .kpi-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
        }
        
        .kpi-value {
            font-size: 2.75rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1;
            margin-bottom: 0.75rem;
        }
        
        .kpi-subtitle {
            font-size: 0.9375rem;
            color: #64748B;
            line-height: 1.5;
        }
        
        /* Status Badges */
        .badge {
            padding: 0.375rem 0.875rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
            margin-right: 0.5rem;
        }
        
        .badge-excellent {
            background: #D1FAE5;
            color: #047857;
        }
        
        .badge-good {
            background: #FEF3C7;
            color: #B45309;
        }
        
        .badge-alert {
            background: #FEE2E2;
            color: #B91C1C;
        }
        
        /* Chart Container */
        .chart-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            height: 100%;
        }
        
        .chart-title {
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 1.5rem;
        }
        
        /* Milestone Card */
        .milestone-card {
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
            color: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
            height: 100%;
        }
        
        .milestone-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            opacity: 0.9;
            margin-bottom: 0.75rem;
        }
        
        .milestone-name {
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
        }
        
        .milestone-date {
            font-size: 1rem;
            opacity: 0.95;
            font-weight: 500;
        }
        
        .milestone-details {
            margin-top: 1.5rem;
            font-size: 0.9375rem;
            opacity: 0.9;
            line-height: 1.6;
        }
        
        /* Equipment Cards */
        .equipment-card {
            background: white;
            border-radius: 12px;
            padding: 1.25rem;
            border: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }
        
        .equipment-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }
        
        .equipment-name {
            font-size: 0.9375rem;
            font-weight: 700;
            color: #0F172A;
        }
        
        .equipment-status {
            font-size: 0.75rem;
            color: #64748B;
        }
        
        .equipment-util {
            font-size: 1.5rem;
            font-weight: 800;
        }
        
        .equipment-bar {
            height: 8px;
            background: #F1F5F9;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .equipment-bar-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================
# Data Helper Functions (From Supabase)
# ============================================

def calculate_total_budget(job):
    """Calculate total budget from job table budget fields"""
    return sum([
        float(job.get("budget_insurance", 0) or 0),
        float(job.get("budget_labor", 0) or 0),
        float(job.get("budget_stamps", 0) or 0),
        float(job.get("budget_material", 0) or 0),
        float(job.get("budget_subs_bond", 0) or 0),
        float(job.get("budget_equipment", 0) or 0)
    ])


def get_job_total_costs(api, job_id):
    """Get actual costs from weekly_costs table"""
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


# ============================================
# Main Application
# ============================================
def main():
    if not check_auth():
        render_login_page()
        return

    branding = get_branding()
    primary_color = branding.get("primary_color", "#6366F1")
    
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
        # Fetch real data from Supabase
        jobs = api.get_jobs() or []
        active_jobs = [j for j in jobs if j.get("status") == "active"]
        
        # Calculate from real data
        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        
        job_costs = {}
        job_budgets = {}
        for job in active_jobs:
            job_costs[job["id"]] = get_job_total_costs(api, job["id"])
            job_budgets[job["id"]] = calculate_total_budget(job)
        
        total_costs = sum(job_costs.values())
        profit = total_contract - total_costs
        margin = (profit / total_contract * 100) if total_contract > 0 else 0
        
        # Calculate aggregate progress
        if active_jobs and len(active_jobs) > 0:
            total_progress = 0
            for job in active_jobs:
                budget = job_budgets.get(job["id"], 0)
                actual = job_costs.get(job["id"], 0)
                if budget > 0:
                    progress = min((actual / budget) * 100, 100)
                    total_progress += progress
            aggregate_progress = total_progress / len(active_jobs)
        else:
            aggregate_progress = 0
        
        # Sample operational data (TODO: Connect to real tables)
        upcoming_payments = [
            {"date": "Oct 22", "amount": 125000},
            {"date": "Oct 25", "amount": 48500},
            {"date": "Oct 28", "amount": 32000}
        ]
        
        safety_incidents = 0
        qc_pass_rate = 95.2
        client_satisfaction = 4.8
        total_employees = 85

        # ============================================
        # SECTION 1: FINANCIAL HEALTH
        # ============================================
        st.markdown("""
        <div class="section-divider">
            <div class="section-icon">💰</div>
            <div class="section-title-text">Financial Health</div>
        </div>
        """, unsafe_allow_html=True)
        
        fin_col1, fin_col2, fin_col3 = st.columns([1, 1, 1.2])
        
        with fin_col1:
            margin_status = "EXCELLENT" if margin >= 15 else "GOOD" if margin >= 10 else "ALERT"
            margin_class = "badge-excellent" if margin >= 15 else "badge-good" if margin >= 10 else "badge-alert"
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Current Revenue & Profit</div>
                <div class="kpi-value">${total_contract:,.0f}</div>
                <div class="kpi-subtitle">
                    <span class="badge {margin_class}">{margin:.1f}% MARGIN</span>
                    <div style="margin-top: 0.5rem; color: #059669; font-weight: 600;">
                        +${profit:,.0f} Profit
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with fin_col2:
            total_due = sum(p['amount'] for p in upcoming_payments)
            next_date = upcoming_payments[0]['date']
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Cash Flow - Payments Due</div>
                <div class="kpi-value">${total_due:,.0f}</div>
                <div class="kpi-subtitle">
                    Next payment: <strong>{next_date}</strong>
                    <div style="margin-top: 0.25rem; color: #64748B;">
                        {len(upcoming_payments)} upcoming payments
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with fin_col3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Monthly Spending Breakdown</div>', unsafe_allow_html=True)
            
            # Create spending chart
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=[50000 + i*1000 for i in range(30)],
                name='Labor', line=dict(color='#6366F1', width=3),
                fill='tonexty', fillcolor='rgba(99, 102, 241, 0.1)'
            ))
            materials = [30000 + i*800 for i in range(30)]
            materials[15] = 65000  # Mid-month spike
            fig.add_trace(go.Scatter(
                x=dates, y=materials,
                name='Materials', line=dict(color='#059669', width=3),
                fill='tonexty', fillcolor='rgba(5, 150, 105, 0.1)'
            ))
            fig.add_trace(go.Scatter(
                x=dates, y=[20000 + i*500 for i in range(30)],
                name='Subcontractors', line=dict(color='#D97706', width=3),
                fill='tonexty', fillcolor='rgba(217, 119, 6, 0.1)'
            ))
            
            fig.update_layout(
                height=280,
                margin=dict(l=10, r=10, t=10, b=30),
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickformat='%b %d', tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor='#F1F5F9', tickformat='$,.0f', tickfont=dict(size=10))
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ============================================
        # SECTION 2: OPERATIONAL PROGRESS
        # ============================================
        st.markdown("""
        <div class="section-divider">
            <div class="section-icon">📊</div>
            <div class="section-title-text">Operational Progress</div>
        </div>
        """, unsafe_allow_html=True)
        
        ops_col1, ops_col2, ops_col3 = st.columns([1, 1, 1.2])
        
        with ops_col1:
            status = "ON TRACK" if aggregate_progress >= 70 else "NEEDS ATTENTION" if aggregate_progress >= 50 else "BEHIND"
            color = "#059669" if aggregate_progress >= 70 else "#D97706" if aggregate_progress >= 50 else "#DC2626"
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Active Jobs Progress</div>
                <div class="kpi-value" style="color: {color};">{aggregate_progress:.0f}%</div>
                <div class="kpi-subtitle">
                    Aggregate completion across all projects
                    <div style="margin-top: 0.5rem; color: {color}; font-weight: 700;">
                        {status}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with ops_col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Phase Breakdown</div>', unsafe_allow_html=True)
            
            fig = go.Figure(data=[go.Pie(
                labels=['Foundation', 'Framing', 'Finishing'],
                values=[25, 45, 30],
                marker=dict(colors=['#6366F1', '#10B981', '#F59E0B']),
                textinfo='label+percent',
                textfont=dict(size=13, color='white'),
                hole=0.4
            )])
            
            fig.update_layout(
                height=260,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=10))
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        with ops_col3:
            st.markdown("""
            <div class="milestone-card">
                <div class="milestone-label">Next Big Milestone</div>
                <div class="milestone-name">Luxury Condo Tower</div>
                <div class="milestone-date">📅 Target: Nov 15, 2024</div>
                <div class="milestone-details">
                    Foundation Complete: 95%<br>
                    Client: Metropolitan Developers
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ============================================
        # SECTION 3: RISK & QUALITY CONTROL
        # ============================================
        st.markdown("""
        <div class="section-divider">
            <div class="section-icon">🛡️</div>
            <div class="section-title-text">Risk & Quality Control</div>
        </div>
        """, unsafe_allow_html=True)
        
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        
        with risk_col1:
            color = "#059669" if safety_incidents == 0 else "#DC2626"
            status = "ZERO INCIDENTS" if safety_incidents == 0 else f"{safety_incidents} INCIDENT{'S' if safety_incidents != 1 else ''}"
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Safety Record (30 Days)</div>
                <div class="kpi-value" style="color: {color};">{safety_incidents}</div>
                <div class="kpi-subtitle">
                    <span class="badge badge-excellent">{status}</span>
                    <div style="margin-top: 0.5rem; color: #64748B;">
                        Industry standard: &lt;0.5/month
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with risk_col2:
            badge_class = "badge-excellent" if qc_pass_rate >= 95 else "badge-good" if qc_pass_rate >= 90 else "badge-alert"
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Quality Control</div>
                <div class="kpi-value">{qc_pass_rate:.1f}%</div>
                <div class="kpi-subtitle">
                    <span class="badge {badge_class}">PASS RATE</span>
                    <div style="margin-top: 0.5rem; color: #64748B;">
                        Workmanship quality checks
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with risk_col3:
            stars = "⭐" * int(client_satisfaction)
            
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Client Satisfaction</div>
                <div class="kpi-value">{client_satisfaction:.1f}/5.0</div>
                <div class="kpi-subtitle">
                    {stars}
                    <div style="margin-top: 0.5rem;">
                        <span class="badge badge-excellent">REPEAT BUSINESS DRIVER</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ============================================
        # SECTION 4: RESOURCE MANAGEMENT
        # ============================================
        st.markdown("""
        <div class="section-divider">
            <div class="section-icon">⚙️</div>
            <div class="section-title-text">Resource Management</div>
        </div>
        """, unsafe_allow_html=True)
        
        resource_col1, resource_col2 = st.columns([1.5, 1])
        
        with resource_col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">Equipment Utilization</div>', unsafe_allow_html=True)
            
            equipment = [
                {"name": "Tower Crane #1", "utilization": 92, "status": "Excellent"},
                {"name": "Scissor Lift #3", "utilization": 78, "status": "Good"},
                {"name": "Boom Lift #2", "utilization": 45, "status": "Underutilized"},
                {"name": "Concrete Mixer", "utilization": 88, "status": "Good"}
            ]
            
            for eq in equipment:
                color = "#059669" if eq["utilization"] >= 80 else "#D97706" if eq["utilization"] >= 60 else "#DC2626"
                st.markdown(f"""
                <div class="equipment-card">
                    <div class="equipment-header">
                        <div>
                            <div class="equipment-name">{eq['name']}</div>
                            <div class="equipment-status">{eq['status']}</div>
                        </div>
                        <div class="equipment-util" style="color: {color};">{eq['utilization']}%</div>
                    </div>
                    <div class="equipment-bar">
                        <div class="equipment-bar-fill" style="width: {eq['utilization']}%; background: {color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with resource_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Workforce</div>
                <div class="kpi-value">{total_employees}</div>
                <div class="kpi-subtitle">
                    Active employees across all projects
                    <div style="margin-top: 0.5rem; color: #64748B;">
                        Field: 68 | Office: 17
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            
            st.markdown("""
            <div class="kpi-card">
                <div class="kpi-label">Capacity for Growth</div>
                <div class="kpi-value">+35%</div>
                <div class="kpi-subtitle">
                    <span class="badge badge-excellent">READY FOR NEW BIDS</span>
                    <div style="margin-top: 0.5rem; color: #64748B;">
                        Can handle 3-4 more projects
                    </div>
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