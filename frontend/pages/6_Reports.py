"""Reports Page - Professional SaaS Colors"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Reports | Elite Wall Pro", page_icon="📈", layout="wide")

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

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

# Import shared styles and sidebar
from components.shared_styles import get_professional_css
from components.sidebar import render_sidebar

# Get branding
tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#6366F1", "company_name": "Elite Wall Pro"})
primary_color = branding.get("primary_color", "#6366F1")

# CRITICAL: Apply CSS BEFORE rendering sidebar
st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)

# Additional Reports page-specific CSS
st.markdown(
    f"""
    <style>
    /* ===== Select Boxes ===== */
    .stSelectbox > div > div {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
    }}

    /* ===== Report Card ===== */
    .report-card {{
        background: #ffffff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }}

    /* ===== Subheaders ===== */
    h3 {{
        color: var(--gray-900) !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }}

    /* ===== Data Tables ===== */
    [data-testid="stDataFrame"] {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        overflow: hidden;
    }}

    /* ===== Download Button ===== */
    .stDownloadButton > button {{
        border-radius: 8px;
        height: 44px;
        font-weight: 600;
        font-size: 0.95rem;
    }}

    /* ===== Empty State ===== */
    .empty-state {{
        text-align: center;
        padding: 60px 30px;
        background: #ffffff;
        border-radius: 12px;
        border: 2px dashed var(--gray-300);
    }}

    .empty-state-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}

    .empty-state-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 0.5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# NOW render sidebar (after all CSS is loaded)
render_sidebar(branding)

# Header
st.markdown("""
<div class='page-header'>
    <div class='page-title'>📈 Reports</div>
</div>
""", unsafe_allow_html=True)

api = st.session_state.api_client

report_type = st.selectbox("Select Report", [
    "Job Profitability Summary",
    "Budget vs Actual by Job",
    "Cost Category Breakdown"
])

try:
    jobs = api.get_jobs()
    active_jobs = [j for j in jobs if j.get("status") == "active"]
    
    if report_type == "Job Profitability Summary":
        st.subheader("Job Profitability Summary")
        
        data = []
        for job in jobs:
            contract = float(job.get("contract_amount", 0) or 0)
            costs = float(job.get("total_costs", 0) or 0)
            profit = contract - costs
            margin = (profit / contract * 100) if contract > 0 else 0
            
            data.append({
                "Job #": job.get("job_number", ""),
                "Name": job.get("job_name", "")[:30],
                "Status": job.get("status", "").title(),
                "Contract": f"${contract:,.0f}",
                "Costs": f"${costs:,.0f}",
                "Profit": f"${profit:,.0f}",
                "Margin": f"{margin:.1f}%"
            })
        
        if data:
            st.dataframe(data, use_container_width=True, hide_index=True)
            
            # Export
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button("📥 Export CSV", csv, "profitability_report.csv", "text/csv")
    
    elif report_type == "Budget vs Actual by Job":
        st.subheader("Budget vs Actual Comparison")
        
        if active_jobs:
            chart_data = []
            for job in active_jobs[:10]:
                chart_data.append({
                    "Job": job.get("job_number", "")[:10],
                    "Budget": float(job.get("total_budget", 0) or 0),
                    "Actual": float(job.get("total_costs", 0) or 0)
                })
            
            df = pd.DataFrame(chart_data)
            fig = go.Figure(data=[
                go.Bar(name="Budget", x=df["Job"], y=df["Budget"], marker_color='#CBD5E1'),
                go.Bar(name="Actual", x=df["Job"], y=df["Actual"], marker_color=primary_color)
            ])
            fig.update_layout(
                barmode="group", 
                title="Budget vs Actual (Top 10 Active Jobs)",
                font=dict(family="Inter, sans-serif", size=12),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "Cost Category Breakdown":
        st.subheader("Cost Category Breakdown")
        
        job_options = {f"{j.get('job_number')} - {j.get('job_name')}": j for j in active_jobs}
        if job_options:
            selected = st.selectbox("Select Job", list(job_options.keys()))
            job = job_options[selected]
            
            try:
                totals = api.get_cost_totals(job["id"])
                actual = totals.get("actual", {})
                
                categories = ["Insurance", "Labor", "Stamps", "Material", "Subs/Bond", "Equipment"]
                keys = ["insurance", "labor", "stamps", "material", "subs_bond", "equipment"]
                values = [float(actual.get(k, 0) or 0) for k in keys]
                
                # Professional color scheme
                colors = ['#10B981', '#6366F1', '#F59E0B', '#8B5CF6', '#EC4899', '#14B8A6']
                
                fig = px.pie(
                    values=values, 
                    names=categories, 
                    title=f"Cost Breakdown: {job.get('job_name', '')}",
                    color_discrete_sequence=colors,
                    hole=0.4
                )
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
                )
                fig.update_layout(
                    font=dict(family="Inter, sans-serif", size=12),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Table
                col1, col2, col3 = st.columns(3)
                budget = totals.get("budget", {})
                variance = totals.get("variance", {})
                
                for i, (cat, key) in enumerate(zip(categories, keys)):
                    with [col1, col2, col3][i % 3]:
                        act = float(actual.get(key, 0) or 0)
                        bud = float(budget.get(key, 0) or 0)
                        var = float(variance.get(key, 0) or 0)
                        st.metric(cat, f"${act:,.0f}", f"${var:,.0f} {'under' if var >= 0 else 'over'}")
            except Exception as e:
                st.error(f"Error loading costs: {e}")
        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>📊</div>
                <div class='empty-state-title'>No active jobs</div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading report: {e}")