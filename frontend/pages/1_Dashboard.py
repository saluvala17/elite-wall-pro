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

st.title("📊 Dashboard")

api = st.session_state.api_client

try:
    jobs = api.get_jobs()
    
    if not jobs:
        st.info("No jobs to display")
        st.stop()
    
    # Calculate metrics
    active_jobs = [j for j in jobs if j.get("status") == "active"]
    completed_jobs = [j for j in jobs if j.get("status") == "completed"]
    
    total_contract = sum(float(j.get("contract_amount", 0) or 0) for j in active_jobs)
    total_costs = sum(float(j.get("total_costs", 0) or 0) for j in active_jobs)
    total_profit = sum(float(j.get("profit", 0) or 0) for j in active_jobs)
    
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Active Jobs", len(active_jobs))
    with col2:
        st.metric("Completed", len(completed_jobs))
    with col3:
        st.metric("Contract Value", f"${total_contract:,.0f}")
    with col4:
        st.metric("Total Costs", f"${total_costs:,.0f}")
    with col5:
        avg_margin = (total_profit / total_contract * 100) if total_contract > 0 else 0
        st.metric("Avg Margin", f"{avg_margin:.1f}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Jobs by Status")
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
    
    with col2:
        st.subheader("Budget vs Actual (Top 5 Active)")
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
    
    st.markdown("---")
    
    # Top Jobs by Profit
    st.subheader("📈 Top Jobs by Profit")
    
    sorted_jobs = sorted(active_jobs, key=lambda x: float(x.get("profit", 0) or 0), reverse=True)[:5]
    
    for job in sorted_jobs:
        profit = float(job.get("profit", 0) or 0)
        margin = float(job.get("profit_margin", 0) or 0)
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.write(f"**{job.get('job_number')}** - {job.get('job_name', '')[:30]}")
        with col2:
            st.write(f"Contract: ${float(job.get('contract_amount', 0) or 0):,.0f}")
        with col3:
            st.write(f"Profit: ${profit:,.0f}")
        with col4:
            color = "green" if margin > 0 else "red"
            st.markdown(f"<span style='color:{color}'>{margin:.1f}%</span>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
