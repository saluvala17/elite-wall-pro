"""
Elite Wall Pro - Streamlit Frontend
Professional Dashboard - Matching Client Design
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
# Professional Dashboard CSS
# --------------------------------------------------
def apply_dashboard_css(primary_color: str):
    st.markdown(
        f"""
        <style>
        /* ===== Color Variables ===== */
        :root {{
            --primary-500: {primary_color};
            --primary-600: #4F46E5;
            --gray-50: #F8FAFC;
            --gray-100: #F1F5F9;
            --gray-200: #E2E8F0;
            --gray-600: #475569;
            --gray-900: #0F172A;
            --success: #10B981;
            --danger: #EF4444;
            --warning: #F59E0B;
        }}
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        .block-container {{
            padding: 2rem 3rem !important;
            max-width: 1600px !important;
        }}
        
        /* ===== Page Header ===== */
        .dashboard-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }}
        
        .dashboard-title {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--gray-900);
        }}
        
        .dashboard-subtitle {{
            font-size: 0.95rem;
            color: var(--gray-600);
            margin-top: 4px;
        }}
        
        .header-actions {{
            display: flex;
            gap: 12px;
        }}
        
        /* ===== Section Titles ===== */
        .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--gray-900);
            margin-bottom: 1.5rem;
        }}
        
        /* ===== Metric Cards ===== */
        [data-testid="stMetric"] {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid var(--gray-200);
        }}
        
        [data-testid="stMetric"] label {{
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            color: var(--gray-600) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--gray-900) !important;
        }}
        
        /* ===== Alert Badges ===== */
        .alert-badges {{
            display: flex;
            gap: 12px;
            margin-bottom: 2rem;
        }}
        
        .alert-badge {{
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        
        .alert-badge-danger {{
            background: #FEE2E2;
            color: #DC2626;
        }}
        
        .alert-badge-warning {{
            background: #FEF3C7;
            color: #D97706;
        }}
        
        /* ===== Job Cards ===== */
        .job-card-new {{
            background: white;
            border: 1px solid var(--gray-200);
            border-left: 4px solid;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 12px;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 24px;
            align-items: center;
        }}
        
        .job-card-new:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        
        .job-info {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .job-title {{
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--gray-900);
        }}
        
        .job-meta {{
            font-size: 0.875rem;
            color: var(--gray-600);
        }}
        
        .job-budget {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .budget-label {{
            font-size: 0.75rem;
            color: var(--gray-600);
            font-weight: 600;
        }}
        
        .budget-amount {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--gray-900);
        }}
        
        .progress-bar {{
            width: 100%;
            height: 6px;
            background: var(--gray-200);
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.3s ease;
        }}
        
        .job-actual {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 8px;
        }}
        
        .actual-amount {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--gray-900);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .margin-badge {{
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .margin-positive {{
            background: #D1FAE5;
            color: var(--success);
        }}
        
        .margin-negative {{
            background: #FEE2E2;
            color: var(--danger);
        }}
        
        .last-cost {{
            font-size: 0.75rem;
            color: var(--gray-600);
        }}
        
        /* ===== Quick Actions Panel ===== */
        .quick-actions-panel {{
            background: white;
            border: 1px solid var(--gray-200);
            border-radius: 12px;
            padding: 24px;
        }}
        
        .quick-actions-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--gray-900);
            margin-bottom: 16px;
        }}
        
        .stButton > button {{
            width: 100% !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
            margin-bottom: 8px !important;
        }}
        
        /* ===== Chart Container ===== */
        .chart-container {{
            background: white;
            border: 1px solid var(--gray-200);
            border-radius: 12px;
            padding: 24px;
            margin-top: 20px;
        }}
        
        .chart-title {{
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--gray-600);
            margin-bottom: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


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

    # Header with actions
    header_left, header_right = st.columns([3, 1])
    
    with header_left:
        st.markdown(f"""
        <div class="dashboard-title">Dashboard</div>
        <div class="dashboard-subtitle">{branding["company_name"]} • Job Costing Overview</div>
        """, unsafe_allow_html=True)
    
    with header_right:
        col_export, col_date = st.columns(2)
        with col_export:
            st.button("📥 Export", use_container_width=True)
        with col_date:
            st.button("📅 Date Range", use_container_width=True)

    st.write("")

    api = st.session_state.api_client

    try:
        jobs = api.get_jobs() or []

        if not jobs:
            st.info("No jobs yet. Create your first job to get started.")
            return

        active_jobs = [j for j in jobs if j.get("status") == "active"]
        
        # Calculate metrics
        total_contract = sum(float(j.get("contract_amount") or 0) for j in active_jobs)
        total_costs = sum(float(j.get("total_costs") or 0) for j in active_jobs)
        total_margin = ((total_contract - total_costs) / total_contract * 100) if total_contract else 0
        over_budget = len([j for j in active_jobs if float(j.get("total_costs") or 0) > float(j.get("total_budget") or 0)])
        near_threshold = len([j for j in active_jobs if 0 <= float(j.get("profit_margin") or 0) < 10])

        # Financial Snapshot
        st.markdown('<div class="section-title">Financial Snapshot</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.metric("ACTIVE JOBS", len(active_jobs))
        
        with c2:
            st.metric("CONTRACT VALUE", f"${total_contract:,.0f}")
        
        with c3:
            st.metric("TOTAL COSTS", f"${total_costs:,.0f}", delta=f"{total_margin:.1f}% margin")
        
        with c4:
            st.metric("RISK ALERTS", over_budget, 
                     delta=f"{over_budget} over budget" if over_budget > 0 else "All on track",
                     delta_color="inverse" if over_budget > 0 else "normal")

        st.write("")

        # Jobs Needing Attention Badges
        if over_budget > 0 or near_threshold > 0:
            badge_html = '<div class="alert-badges">'
            if over_budget > 0:
                badge_html += f'<span class="alert-badge alert-badge-danger">🔴 {over_budget} Job{"s" if over_budget > 1 else ""} Over Budget</span>'
            if near_threshold > 0:
                badge_html += f'<span class="alert-badge alert-badge-warning">⚠️ {near_threshold} Job{"s" if near_threshold > 1 else ""} Near Margin Threshold</span>'
            badge_html += '</div>'
            st.markdown(badge_html, unsafe_allow_html=True)

        # Main content area (2 columns)
        col_main, col_sidebar = st.columns([2.5, 1], gap="large")

        with col_main:
            st.markdown('<div class="section-title">Active Jobs</div>', unsafe_allow_html=True)
            
            # Display jobs
            for job in active_jobs:
                budget = float(job.get("total_budget") or 0)
                actual = float(job.get("total_costs") or 0)
                contract = float(job.get("contract_amount") or 0)
                margin = float(job.get("profit_margin") or 0)
                
                # Calculate progress percentage
                progress_pct = (actual / budget * 100) if budget > 0 else 0
                is_over_budget = actual > budget
                
                # Border color
                border_color = "#EF4444" if is_over_budget else "#10B981"
                progress_color = "#EF4444" if is_over_budget else "#10B981"
                
                st.markdown(f"""
                <div class="job-card-new" style="border-left-color: {border_color}">
                    <div class="job-info">
                        <div class="job-title">{job.get("job_name", "Untitled")}</div>
                        <div class="job-meta">#{job.get("job_number", "N/A")} · {job.get("customer_name", "No customer")}</div>
                        <div class="job-budget">
                            <span class="budget-label">Budget</span>
                            <span class="budget-amount">${budget:,.0f}</span>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {min(progress_pct, 100)}%; background-color: {progress_color}"></div>
                            </div>
                        </div>
                    </div>
                    <div class="job-actual">
                        <span class="actual-amount">
                            ${actual:,.0f}
                        </span>
                        <span class="margin-badge {'margin-negative' if is_over_budget else 'margin-positive'}">
                            {'⚠️ Over Budget' if is_over_budget else f'✓ {margin:.1f}% margin'}
                        </span>
                        <span class="last-cost">Last cost: 3 days ago</span>
                    </div>
                    <div style="text-align: right;">
                        <div class="budget-label">Actual</div>
                        <div class="budget-amount" style="font-size: 1.3rem;">$ {actual:,.0f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_sidebar:
            # Quick Actions
            st.markdown("""
            <div class="quick-actions-panel">
                <div class="quick-actions-title">Quick Actions</div>
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
            
            # Budget vs Actual Chart
            st.markdown("""
            <div class="chart-container">
                <div class="chart-title">Budget vs Actual (Top 5)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create simple bar chart
            top_5 = active_jobs[:5]
            if top_5:
                chart_data = []
                for j in top_5:
                    chart_data.append({
                        "Job": j.get("job_number", "")[:10],
                        "Budget": float(j.get("total_budget") or 0),
                        "Actual": float(j.get("total_costs") or 0)
                    })
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=[d["Job"] for d in chart_data],
                        y=[d["Budget"] for d in chart_data],
                        name="Budget",
                        marker_color='#D1D5DB',
                        width=0.4
                    ),
                    go.Bar(
                        x=[d["Job"] for d in chart_data],
                        y=[d["Actual"] for d in chart_data],
                        name="Actual",
                        marker_color='#10B981',
                        width=0.4
                    )
                ])
                
                fig.update_layout(
                    barmode='group',
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=30),
                    showlegend=False,
                    plot_bgcolor='white',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#F1F5F9')
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error(f"⚠️ Error loading dashboard: {e}")


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    main()