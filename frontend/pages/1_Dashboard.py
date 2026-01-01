"""Dashboard Page"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Dashboard | Elite Wall Pro", page_icon="📊", layout="wide")

# Check auth
if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

# Get branding
tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})

render_sidebar(branding)

# Global UI styles (QuickBooks-inspired card layout, spacing, type)
st.markdown(
        f"""
        <style>
        :root{{ --accent: #2CA01C; --muted-1: #E5E7EB; --muted-2: #F3F4F6; --card-radius:8px; }}
        html, body {{font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;}}
        .page-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;gap:16px;}}
        .title{{font-size:22px;font-weight:700;color:#111827;display:flex;align-items:center;gap:8px}}
        .subtle{{color:#6B7280;font-size:13px}}
        .action-pill{{background:var(--muted-2);border:1px solid var(--muted-1);padding:6px 10px;border-radius:6px;color:#111827;font-size:13px}}
        .card{{background:#ffffff;border:1px solid var(--muted-1);border-radius:var(--card-radius);padding:18px;margin-bottom:18px;box-shadow:0 1px 2px rgba(16,24,40,0.04)}}
        .kpi-row{{display:flex;gap:16px;align-items:stretch}}
        .kpi{{flex:1;background:transparent;padding:12px;border-radius:6px;border:1px solid #F3F4F6;display:flex;flex-direction:column;gap:6px}}
        .kpi .label{font-size:13px;color:#6B7280}
        .kpi .value{font-size:18px;font-weight:700;color:#111827}
        .section-title{font-size:16px;font-weight:600;color:#111827;margin-bottom:12px}
        .job-row{display:flex;align-items:center;gap:12px;padding:12px;border-radius:6px;border:1px solid var(--muted-2);margin-bottom:8px}
        .profit-positive{color:var(--accent);font-weight:600}
        .profit-negative{color:#DC2626;font-weight:600}
        </style>
        """,
        unsafe_allow_html=True,
)

# Header (left-aligned, simple action pill on right)
st.markdown("""
<div class='page-header'>
    <div>
        <div class='title'>📊 Dashboard</div>
        <div class='subtle'>Overview of jobs, costs, and margins</div>
    </div>
    <div>
        <span class='action-pill'>Export</span>
    </div>
</div>
""", unsafe_allow_html=True)

api = st.session_state.api_client

try:
    jobs = api.get_jobs()
    
    if not jobs:
                st.markdown("""
                <div class='card'>
                    <div style='display:flex;flex-direction:column;gap:8px;'>
                        <div style='font-weight:700;color:#111827'>No jobs to display</div>
                        <div style='color:#6B7280'>Once jobs are added you'll see KPIs, charts, and top jobs here.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.stop()
    
    # Calculate metrics
    active_jobs = [j for j in jobs if j.get("status") == "active"]
    completed_jobs = [j for j in jobs if j.get("status") == "completed"]
    
    total_contract = sum(float(j.get("contract_amount", 0) or 0) for j in active_jobs)
    total_costs = sum(float(j.get("total_costs", 0) or 0) for j in active_jobs)
    total_profit = sum(float(j.get("profit", 0) or 0) for j in active_jobs)
    
    # KPIs - render inside a card row
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    cols = st.columns(5)
    kpi_values = [
        ("Active Jobs", len(active_jobs)),
        ("Completed", len(completed_jobs)),
        ("Contract Value", f"${total_contract:,.0f}"),
        ("Total Costs", f"${total_costs:,.0f}"),
        ("Avg Margin", f"{((total_profit / total_contract * 100) if total_contract>0 else 0):.1f}%"),
    ]
    for c, (label, value) in zip(cols, kpi_values):
        with c:
            st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    # Charts - each chart in its own card
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Jobs by Status</div>", unsafe_allow_html=True)
        status_counts = {}
        for j in jobs:
            s = j.get("status", "unknown")
            status_counts[s] = status_counts.get(s, 0) + 1
        
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Budget vs Actual (Top 5 Active)</div>", unsafe_allow_html=True)
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
                go.Bar(name="Budget", x=df["Job"], y=df["Budget"]),
                go.Bar(name="Actual", x=df["Job"], y=df["Actual"])
            ])
            fig.update_layout(barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    # Top Jobs by Profit
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📈 Top Jobs by Profit</div>", unsafe_allow_html=True)
    
    sorted_jobs = sorted(active_jobs, key=lambda x: float(x.get("profit", 0) or 0), reverse=True)[:5]
    
    for job in sorted_jobs:
        profit = float(job.get("profit", 0) or 0)
        margin = float(job.get("profit_margin", 0) or 0)
        
        cols = st.columns([3, 2, 2, 2])
        with cols[0]:
            st.markdown(f"<div class='job-row'><div style='flex:1'><div style='font-weight:700'>{job.get('job_number')}</div><div class='subtle'>{job.get('job_name','')[:60]}</div></div></div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<div class='subtle'>Contract</div><div style='font-weight:600'>${float(job.get('contract_amount', 0) or 0):,.0f}</div>", unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"<div class='subtle'>Profit</div><div style='font-weight:600'>${profit:,.0f}</div>", unsafe_allow_html=True)
        with cols[3]:
            cls = 'profit-positive' if margin>0 else 'profit-negative'
            st.markdown(f"<div class='subtle'>Margin</div><div class='{cls}'>{margin:.1f}%</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
