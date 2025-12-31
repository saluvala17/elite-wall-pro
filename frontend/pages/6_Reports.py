"""Reports Page"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Reports | Elite Wall Pro", page_icon="📈", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

st.title("📈 Reports")

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
                go.Bar(name="Budget", x=df["Job"], y=df["Budget"], marker_color="#4A7C59"),
                go.Bar(name="Actual", x=df["Job"], y=df["Actual"], marker_color="#8B4513")
            ])
            fig.update_layout(barmode="group", title="Budget vs Actual (Top 10 Active Jobs)")
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
                
                fig = px.pie(values=values, names=categories, title=f"Cost Breakdown: {job.get('job_name', '')}")
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
            st.info("No active jobs")

except Exception as e:
    st.error(f"Error loading report: {e}")
