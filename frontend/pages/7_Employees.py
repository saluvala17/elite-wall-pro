"""Employees Page"""
import streamlit as st

st.set_page_config(page_title="Employees | Elite Wall Pro", page_icon="👷", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

st.title("👷 Employees")

api = st.session_state.api_client
can_edit = st.session_state.get("user", {}).get("role", "") in ("admin", "super_admin", "manager")

tab1, tab2 = st.tabs(["📋 All Employees", "➕ New Employee"]) if can_edit else st.tabs(["📋 All Employees"])

with tab1:
    try:
        employees = api.get_employees()
        if employees:
            for e in employees:
                name = f"{e.get('first_name', '')} {e.get('last_name', '')}"
                with st.expander(f"{name} - {e.get('role', 'Employee')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {e.get('employee_id', 'N/A')}")
                        st.write(f"**Email:** {e.get('email', 'N/A')}")
                        st.write(f"**Phone:** {e.get('phone', 'N/A')}")
                    with col2:
                        st.write(f"**Department:** {e.get('department', 'N/A')}")
                        st.write(f"**Hire Date:** {e.get('hire_date', 'N/A')}")
                        rate = e.get('hourly_rate')
                        st.write(f"**Rate:** ${float(rate):,.2f}/hr" if rate else "**Rate:** N/A")
        else:
            st.info("No employees found")
    except Exception as e:
        st.error(f"Error: {e}")

if can_edit:
    with tab2:
        with st.form("new_employee"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *")
                last_name = st.text_input("Last Name *")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
            with col2:
                employee_id = st.text_input("Employee ID")
                role = st.text_input("Role/Title")
                department = st.text_input("Department")
                hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=1.0)
            
            if st.form_submit_button("Create Employee", type="primary"):
                if first_name and last_name:
                    try:
                        api.create_employee({
                            "first_name": first_name, "last_name": last_name,
                            "email": email, "phone": phone, "employee_id": employee_id,
                            "role": role, "department": department, "hourly_rate": hourly_rate
                        })
                        st.success("Employee created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("First and Last name are required")
