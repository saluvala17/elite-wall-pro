"""Customers Page"""
import streamlit as st

st.set_page_config(page_title="Customers | Elite Wall Pro", page_icon="👥", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

st.title("👥 Customers")

api = st.session_state.api_client
can_edit = st.session_state.get("user", {}).get("role", "") in ("admin", "super_admin", "manager")

tab1, tab2 = st.tabs(["📋 All Customers", "➕ New Customer"]) if can_edit else st.tabs(["📋 All Customers"])

with tab1:
    try:
        customers = api.get_customers()
        if customers:
            for c in customers:
                with st.expander(f"{c.get('name', 'Unknown')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Contact:** {c.get('contact_name', 'N/A')}")
                        st.write(f"**Email:** {c.get('email', 'N/A')}")
                    with col2:
                        st.write(f"**Phone:** {c.get('phone', 'N/A')}")
                        st.write(f"**Address:** {c.get('address', 'N/A')}")
        else:
            st.info("No customers found")
    except Exception as e:
        st.error(f"Error: {e}")

if can_edit:
    with tab2:
        with st.form("new_customer"):
            name = st.text_input("Company Name *")
            contact = st.text_input("Contact Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            
            if st.form_submit_button("Create Customer", type="primary"):
                if name:
                    try:
                        api.create_customer({"name": name, "contact_name": contact, "email": email, "phone": phone, "address": address})
                        st.success("Customer created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Name is required")
