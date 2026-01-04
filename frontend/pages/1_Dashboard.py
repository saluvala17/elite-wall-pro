"""Dashboard Page - Analytics & Insights (CORRECTED)"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Dashboard | Elite Wall Pro", page_icon="📊", layout="wide")

# CRITICAL: Hide Streamlit defaults FIRST
st.markdown(
    """
    <style>
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        header { visibility: hidden !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Check auth
if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

# Import shared styles and sidebar
from components.shared_styles import get_professional_css
from components.sidebar import render_sidebar

# Get branding
tenant = st.session_state.get("tenant") or {}
branding = tenant.get("branding", {"primary_color": "#6366F1", "company_name": "Elite Wall Pro"})
primary_color = branding.get("primary_color", "#6366F1")

# CRITICAL: Apply CSS BEFORE rendering sidebar
st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)

# Dashboard-specific CSS
st.markdown(
    f"""
    <style>
    /* Section Headers */
    .section-header {{
        font-size: 1.125rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E2E8F0;
    }}

    /* Job Cards */
    .job-summary-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }}

    .job-summary-card:hover {{
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-color: #CBD5E1;
    }}

    .job-number {{
        font-weight: 700;
        color: #0F172A;
        font-size: 1rem;
    }}

    .job-name {{
        color: #64748B;
        font-size: 0.875rem;
    }}

    .metric-label {{
        font-size: 0.6875rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }}

    .metric-value {{
        font-weight: 600;
        color: #0F172A;
        font-size: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# NOW render sidebar
render_sidebar(branding)


# --------------------------------------------------
# CRITICAL: Helper Functions for Data Calculation
# --------------------------------------------------
def calculate_total_budget(job):
    """Calculate total budget from all budget fields in jobs table"""
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
        return 0


def get_job_total_costs(api, job_id):
    """Get actual total costs for a job from weekly_costs table"""
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
# Main Dashboard
# --------------------------------------------------

# Header
st.title("📊 Analytics Dashboard")
st.caption(f"{branding['company_name']} • Performance Insights & Trends")

st.write("")

api = st.session_state.api_client

try:
    jobs = api.get_jobs() or []
    
    if not jobs:
        st.info("📋 No jobs yet. Create your first job to see analytics.")
        if st.button("➕ Create First Job", type="primary"):
            st.switch_page("pages/2_Jobs.py")
        st.stop()
    
    # ============================================
    # CRITICAL: Calculate all costs upfront
    # ============================================
    job_costs = {}
    job_budgets = {}
    
    for job in jobs:
        job_id = job["id"]
        job_costs[job_id] = get_job_total_costs(api, job_id)
        job_budgets[job_id] = calculate_total_budget(job)
    
    # Segment jobs by status
    active_jobs = [j for j in jobs if j.get("status") == "active"]
    completed_jobs = [j for j in jobs if j.get("status") == "completed"]
    estimate_jobs = [j for j in jobs if j.get("status") == "estimate"]
    on_hold_jobs = [j for j in jobs if j.get("status") == "on_hold"]
    
    # ============================================
    # Calculate financial metrics CORRECTLY
    # ============================================
    total_contract = sum(float(j.get("contract_amount", 0) or 0) for j in active_jobs)
    total_costs = sum(job_costs.get(j["id"], 0) for j in active_jobs)
    total_profit = total_contract - total_costs
    avg_margin = ((total_profit / total_contract * 100) if total_contract > 0 else 0)
    
    # Completed jobs metrics
    completed_contract = sum(float(j.get("contract_amount", 0) or 0) for j in completed_jobs)
    completed_costs = sum(job_costs.get(j["id"], 0) for j in completed_jobs)
    completed_profit = completed_contract - completed_costs
    
    # ============================================
    # KPI METRICS
    # ============================================
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Active Jobs", len(active_jobs))
    
    with col2:
        st.metric("Completed", len(completed_jobs))
    
    with col3:
        st.metric("Total Revenue", f"${total_contract:,.0f}")
    
    with col4:
        st.metric("Total Costs", f"${total_costs:,.0f}")
    
    with col5:
        st.metric("Avg Margin", f"{avg_margin:.1f}%",
                 delta=f"{avg_margin:.1f}%",
                 delta_color="normal" if avg_margin > 0 else "inverse")
    
    st.write("")
    st.write("")
    
    # ============================================
    # CHARTS SECTION
    # ============================================
    chart_col1, chart_col2 = st.columns(2, gap="large")
    
    with chart_col1:
        st.markdown('<div class="section-header">Jobs by Status</div>', unsafe_allow_html=True)
        
        # Count jobs by status
        status_counts = {
            'Active': len(active_jobs),
            'Completed': len(completed_jobs),
            'Estimate': len(estimate_jobs),
            'On Hold': len(on_hold_jobs)
        }
        
        # Remove zero counts
        status_counts = {k: v for k, v in status_counts.items() if v > 0}
        
        if status_counts:
            # Professional color scheme
            colors = ['#10B981', '#6366F1', '#F59E0B', '#8B5CF6']
            
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                color_discrete_sequence=colors,
                hole=0.4
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
            )
            fig.update_layout(
                showlegend=True,
                height=350,
                margin=dict(t=20, b=20, l=20, r=20),
                font=dict(family="Inter, sans-serif", size=12),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No job status data available")
    
    with chart_col2:
        st.markdown('<div class="section-header">Budget vs Actual (Top 5)</div>', unsafe_allow_html=True)
        
        if active_jobs:
            # Get top 5 by contract value
            top_5 = sorted(active_jobs, key=lambda x: float(x.get("contract_amount") or 0), reverse=True)[:5]
            
            labels = []
            budgets = []
            actuals = []
            
            for job in top_5:
                labels.append(job.get("job_number", "N/A")[:12])
                budgets.append(job_budgets.get(job["id"], 0))
                actuals.append(job_costs.get(job["id"], 0))
            
            fig = go.Figure(data=[
                go.Bar(
                    name="Budget",
                    x=labels,
                    y=budgets,
                    marker_color='#CBD5E1',
                    hovertemplate='<b>%{x}</b><br>Budget: $%{y:,.0f}<extra></extra>'
                ),
                go.Bar(
                    name="Actual",
                    x=labels,
                    y=actuals,
                    marker_color=primary_color,
                    hovertemplate='<b>%{x}</b><br>Actual: $%{y:,.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                barmode="group",
                height=350,
                margin=dict(t=20, b=60, l=60, r=20),
                font=dict(family="Inter, sans-serif", size=12),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                xaxis=dict(title="", tickangle=-45),
                yaxis=dict(title="Amount ($)", tickformat='$,.0f')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No active jobs to display")
    
    st.write("")
    st.write("")
    
    # ============================================
    # PROFITABILITY ANALYSIS
    # ============================================
    st.markdown('<div class="section-header">💰 Profitability Analysis</div>', unsafe_allow_html=True)
    
    # Calculate profitability for each active job
    job_profitability = []
    for job in active_jobs:
        job_id = job["id"]
        contract = float(job.get("contract_amount") or 0)
        costs = job_costs.get(job_id, 0)
        budget = job_budgets.get(job_id, 0)
        profit = contract - costs
        margin = ((profit / contract * 100) if contract > 0 else 0)
        
        job_profitability.append({
            'job': job,
            'contract': contract,
            'budget': budget,
            'costs': costs,
            'profit': profit,
            'margin': margin
        })
    
    # Sort by profit
    job_profitability.sort(key=lambda x: x['profit'], reverse=True)
    
    # Display top 5 profitable jobs
    if job_profitability:
        st.markdown("**Top Performing Jobs**")
        
        for item in job_profitability[:5]:
            job = item['job']
            
            with st.container():
                st.markdown('<div class="job-summary-card">', unsafe_allow_html=True)
                
                col_name, col_contract, col_costs, col_profit, col_margin = st.columns([2, 1.5, 1.5, 1.5, 1])
                
                with col_name:
                    st.markdown(f'<div class="job-number">#{job.get("job_number", "N/A")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="job-name">{job.get("job_name", "Untitled")[:40]}</div>', unsafe_allow_html=True)
                
                with col_contract:
                    st.markdown('<div class="metric-label">CONTRACT</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">${item["contract"]:,.0f}</div>', unsafe_allow_html=True)
                
                with col_costs:
                    st.markdown('<div class="metric-label">COSTS</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">${item["costs"]:,.0f}</div>', unsafe_allow_html=True)
                
                with col_profit:
                    st.markdown('<div class="metric-label">PROFIT</div>', unsafe_allow_html=True)
                    profit_icon = "🟢" if item['profit'] > 0 else "🔴"
                    st.markdown(f'<div class="metric-value">{profit_icon} ${item["profit"]:,.0f}</div>', unsafe_allow_html=True)
                
                with col_margin:
                    st.markdown('<div class="metric-label">MARGIN</div>', unsafe_allow_html=True)
                    if item['margin'] > 0:
                        st.success(f"{item['margin']:.1f}%")
                    else:
                        st.error(f"{item['margin']:.1f}%")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
        
        # Show worst performing if any have negative margins
        negative_margin_jobs = [item for item in job_profitability if item['margin'] < 0]
        
        if negative_margin_jobs:
            st.write("")
            st.markdown("**⚠️ Jobs Needing Attention**")
            st.warning(f"{len(negative_margin_jobs)} job(s) with negative margins")
            
            for item in negative_margin_jobs[:3]:
                job = item['job']
                
                with st.container():
                    st.markdown('<div class="job-summary-card">', unsafe_allow_html=True)
                    
                    col_name, col_contract, col_costs, col_loss, col_margin = st.columns([2, 1.5, 1.5, 1.5, 1])
                    
                    with col_name:
                        st.markdown(f'<div class="job-number">#{job.get("job_number", "N/A")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="job-name">{job.get("job_name", "Untitled")[:40]}</div>', unsafe_allow_html=True)
                    
                    with col_contract:
                        st.markdown('<div class="metric-label">CONTRACT</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">${item["contract"]:,.0f}</div>', unsafe_allow_html=True)
                    
                    with col_costs:
                        st.markdown('<div class="metric-label">COSTS</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">${item["costs"]:,.0f}</div>', unsafe_allow_html=True)
                    
                    with col_loss:
                        st.markdown('<div class="metric-label">LOSS</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">🔴 ${abs(item["profit"]):,.0f}</div>', unsafe_allow_html=True)
                    
                    with col_margin:
                        st.markdown('<div class="metric-label">MARGIN</div>', unsafe_allow_html=True)
                        st.error(f"{item['margin']:.1f}%")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.write("")
    
    else:
        st.info("No active jobs to analyze")
    
    st.write("")
    st.write("")
    
    # ============================================
    # COMPLETED JOBS SUMMARY
    # ============================================
    if completed_jobs:
        st.markdown('<div class="section-header">✅ Completed Jobs Summary</div>', unsafe_allow_html=True)
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Completed Jobs", len(completed_jobs))
        
        with summary_col2:
            st.metric("Total Revenue", f"${completed_contract:,.0f}")
        
        with summary_col3:
            st.metric("Total Costs", f"${completed_costs:,.0f}")
        
        with summary_col4:
            completed_margin = ((completed_profit / completed_contract * 100) if completed_contract > 0 else 0)
            st.metric("Total Profit", f"${completed_profit:,.0f}",
                     delta=f"{completed_margin:.1f}% margin")

except Exception as e:
    st.error(f"⚠️ Error loading dashboard analytics: {str(e)}")
    
    with st.expander("Debug Information"):
        import traceback
        st.code(f"""
Error: {str(e)}

Jobs fetched: {len(jobs) if 'jobs' in locals() else 'N/A'}
Active jobs: {len(active_jobs) if 'active_jobs' in locals() else 'N/A'}

Traceback:
{traceback.format_exc()}
        """)
    
    if st.button("🔄 Retry"):
        st.rerun()