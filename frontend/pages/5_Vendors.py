"""Vendors Page"""
import streamlit as st

st.set_page_config(page_title="Vendors | Elite Wall Pro", page_icon="🏪", layout="wide")

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

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

st.title("🏪 Vendors")

api = st.session_state.api_client
can_edit = st.session_state.get("user", {}).get("role", "") in ("admin", "super_admin", "manager")

tab1, tab2 = st.tabs(["📋 All Vendors", "➕ New Vendor"]) if can_edit else st.tabs(["📋 All Vendors"])

with tab1:
    try:
        vendors = api.get_vendors()
        if vendors:
            for v in vendors:
                with st.expander(f"{v.get('name', 'Unknown')} ({v.get('vendor_type', 'General')})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Contact:** {v.get('contact_name', 'N/A')}")
                        st.write(f"**Email:** {v.get('email', 'N/A')}")
                    with col2:
                        st.write(f"**Phone:** {v.get('phone', 'N/A')}")
                        st.write(f"**Payment Terms:** {v.get('payment_terms', 'N/A')}")
        else:
            st.info("No vendors found")
    except Exception as e:
        st.error(f"Error: {e}")

if can_edit:
    with tab2:
        with st.form("new_vendor"):
            name = st.text_input("Vendor Name *")
            vendor_type = st.selectbox("Type", ["Material Supplier", "Subcontractor", "Equipment Rental", "Other"])
            contact = st.text_input("Contact Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            
            if st.form_submit_button("Create Vendor", type="primary"):
                if name:
                    try:
                        api.create_vendor({"name": name, "vendor_type": vendor_type, "contact_name": contact, "email": email, "phone": phone})
                        st.success("Vendor created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Name is required")
