"""Sidebar Component"""
import streamlit as st
from components.auth import logout


def render_sidebar(branding: dict):
    """Render application sidebar"""
    with st.sidebar:
        # Logo/Company Name
        primary_color = branding.get("primary_color", "#4A7C59")
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        if branding.get("logo_url"):
            st.image(branding["logo_url"], width=150)
        else:
            # Default logo
            st.markdown(f"""
            <div style="padding: 0.5rem 0 1rem 0;">
                <div style="display: flex; flex-direction: column; gap: 3px;">
                    <div style="width: 35px; height: 7px; background: {primary_color};"></div>
                    <div style="width: 35px; height: 7px; background: {primary_color};"></div>
                    <div style="width: 35px; height: 7px; background: {primary_color};"></div>
                </div>
                <div style="margin-top: 10px;">
                    <span style="color: {primary_color}; font-size: 1.2rem; font-weight: 700;">{company_name}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # User info
        user = st.session_state.get("user", {})
        if user:
            st.markdown(f"""
            <div style="background: {primary_color}; color: white; padding: 0.5rem 0.75rem; 
                        border-radius: 6px; margin-bottom: 1rem;">
                <div style="font-weight: 600;">👤 {user.get('name', 'User')}</div>
                <div style="font-size: 0.8rem; opacity: 0.9;">{user.get('role', 'Employee').title()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/2_Jobs.py", label="📋 Jobs")
        st.page_link("pages/3_Cost_Entry.py", label="💰 Cost Entry")
        st.page_link("pages/4_Customers.py", label="👥 Customers")
        st.page_link("pages/5_Vendors.py", label="🏪 Vendors")
        st.page_link("pages/6_Reports.py", label="📈 Reports")
        st.page_link("pages/7_Employees.py", label="👷 Employees")
        
        # Admin pages
        user_role = user.get("role", "")
        if user_role in ("admin", "super_admin"):
            st.markdown("---")
            st.markdown("**Admin**")
            st.page_link("pages/8_Settings.py", label="⚙️ Settings")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.caption(f"v2.0 | {company_name}")
