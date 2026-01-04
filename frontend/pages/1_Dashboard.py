"""Dashboard Page - Professional SaaS Colors"""
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

# Additional Dashboard page-specific CSS
st.markdown(
    f"""
    <style>
    /* ===== Export Button ===== */
    .export-button {{
        background: #ffffff;
        border: 1px solid var(--gray-300);
        padding: 10px 20px;
        border-radius: 8px;
        color: var(--gray-600);
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }}

    .export-button:hover {{
        background: var(--gray-50);
        border-color: var(--gray-600);
    }}

    /* ===== Section Headers ===== */
    .section-header {{
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--gray-200);
    }}

    /* ===== Job Table ===== */
    .job-table-row {{
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 16px;
        padding: 16px 20px;
        background: #ffffff;
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }}

    .job-table-row:hover {{
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }}

    .job-number {{
        font-weight: 700;
        color: var(--gray-900);
        font-size: 1rem;
    }}

    .job-name {{
        color: var(--gray-600);
        font-size: 0.875rem;
    }}

    .metric-label {{
        font-size: 0.75rem;
        color: var(--gray-600);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }}

    .metric-value {{
        font-weight: 600;
        color: var(--gray-900);
        font-size: 1rem;
    }}

    .profit-positive {{
        color: var(--success);
        font-weight: 600;
    }}

    .profit-negative {{
        color: var(--danger);
        font-weight: 600;
    }}

    /* ===== Responsive ===== */
    @media (max-width: 768px) {{
        .job-table-row {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# NOW render sidebar (after all CSS is loaded)
render_sidebar(branding)

# Enhanced Header
st.markdown(f"""
<div class='page-header'>
    <div>
        <div class='page-title'>📊 Dashboard</div>
        <div class='page-subtitle'>Overview of jobs, costs, and margins</div>
    </div>
    <div>
        <button class='export-button'>📥 Export</button>
    </div>
</div>
""", unsafe_allow_html=True)

api = st.session_state.api_client

try:
    jobs = api.get_jobs()
    
    if not jobs:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>📋</div>
            <div class='empty-state-title'>No jobs to display</div>
            <div class='empty-state-text'>Once jobs are added you'll see KPIs, charts, and insights here.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Calculate metrics
    active_jobs = [j for j in jobs if j.get("status") == "active"]
    completed_jobs = [j for j in jobs if j.get("status") == "completed"]
    
    total_contract = sum(float(j.get("contract_amount", 0) or 0) for j in active_jobs)
    total_costs = sum(float(j.get("total_costs", 0) or 0) for j in active_jobs)
    total_profit = sum(float(j.get("profit", 0) or 0) for j in active_jobs)
    avg_margin = ((total_profit / total_contract * 100) if total_contract > 0 else 0)
    
    # KPI Section
    cols = st.columns(5)
    kpi_data = [
        ("Active Jobs", f"{len(active_jobs)}", None),
        ("Completed", f"{len(completed_jobs)}", None),
        ("Contract Value", f"${total_contract:,.0f}", None),
        ("Total Costs", f"${total_costs:,.0f}", None),
        ("Avg Margin", f"{avg_margin:.1f}%", f"{avg_margin:.1f}%" if avg_margin > 0 else None),
    ]
    
    for col, (label, value, delta) in zip(cols, kpi_data):
        with col:
            st.metric(label, value, delta=delta)
    
    st.write("")
    st.write("")
    
    # Charts Section
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="section-header">Jobs by Status</div>', unsafe_allow_html=True)
        
        status_counts = {}
        for j in jobs:
            s = j.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        
        # Professional color scheme
        colors = {
            'active': '#10b981',
            'completed': '#6366F1',
            'estimate': '#F59E0B',
            'on_hold': '#8b5cf6',
            'unknown': '#6b7280'
        }
        color_sequence = [colors.get(status, '#6b7280') for status in status_counts.keys()]
        
        fig = px.pie(
            values=list(status_counts.values()),
            names=[s.replace('_', ' ').title() for s in status_counts.keys()],
            color_discrete_sequence=color_sequence,
            hole=0.4
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        fig.update_layout(
            showlegend=True,
            height=350,
            margin=dict(t=20, b=20, l=20, r=20),
            font=dict(family="Inter, sans-serif", size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Budget vs Actual (Top 5)</div>', unsafe_allow_html=True)
        
        chart_data = []
        for j in active_jobs[:5]:
            chart_data.append({
                "Job": j.get("job_number", "")[:15],
                "Budget": float(j.get("total_budget", 0) or 0),
                "Actual": float(j.get("total_costs", 0) or 0)
            })
        
        if chart_data:
            df = pd.DataFrame(chart_data)
            fig = go.Figure(data=[
                go.Bar(
                    name="Budget",
                    x=df["Job"],
                    y=df["Budget"],
                    marker_color='#CBD5E1',
                    hovertemplate='<b>%{x}</b><br>Budget: $%{y:,.0f}<extra></extra>'
                ),
                go.Bar(
                    name="Actual",
                    x=df["Job"],
                    y=df["Actual"],
                    marker_color=primary_color,
                    hovertemplate='<b>%{x}</b><br>Actual: $%{y:,.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                barmode="group",
                height=350,
                margin=dict(t=20, b=40, l=40, r=20),
                font=dict(family="Inter, sans-serif", size=12),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title=""),
                yaxis=dict(title="Amount ($)")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No budget data available for active jobs")
    
    st.write("")
    
    # Top Jobs Section
    st.markdown('<div class="section-header">📈 Top Jobs by Profit</div>', unsafe_allow_html=True)
    
    sorted_jobs = sorted(active_jobs, key=lambda x: float(x.get("profit", 0) or 0), reverse=True)[:5]
    
    if sorted_jobs:
        for job in sorted_jobs:
            profit = float(job.get("profit", 0) or 0)
            margin = float(job.get("profit_margin", 0) or 0)
            contract = float(job.get("contract_amount", 0) or 0)
            
            margin_class = 'profit-positive' if margin > 0 else 'profit-negative'
            
            st.markdown(f"""
            <div class='job-table-row'>
                <div class='job-info'>
                    <div class='job-number'>{job.get('job_number', 'N/A')}</div>
                    <div class='job-name'>{job.get('job_name', 'Untitled')[:60]}</div>
                </div>
                <div class='job-metric'>
                    <div class='metric-label'>Contract</div>
                    <div class='metric-value'>${contract:,.0f}</div>
                </div>
                <div class='job-metric'>
                    <div class='metric-label'>Profit</div>
                    <div class='metric-value'>${profit:,.0f}</div>
                </div>
                <div class='job-metric'>
                    <div class='metric-label'>Margin</div>
                    <div class='{margin_class}'>{margin:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active jobs with profit data")

except Exception as e:
    st.error(f"⚠️ Error loading dashboard: {e}")
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Retry", use_container_width=True):
            st.rerun()