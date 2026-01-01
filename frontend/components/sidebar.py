"""Sidebar Component"""
import streamlit as st
from components.auth import logout


def render_sidebar(branding: dict):
    """Render application sidebar"""
    with st.sidebar:
        # QuickBooks-inspired sidebar styles (UI-only)
        st.markdown(
            """
            <style>
            .stSidebar > div {background: #ffffff !important;}
            .ewp-sidebar-logo{padding:12px 6px 8px 6px;margin-bottom:6px}
            .ewp-company{font-weight:700;color:#111827;font-size:1rem}
            .ewp-user-pill{background:#F3F4F6;padding:8px;border-radius:8px;margin-bottom:8px}
            .ewp-nav a{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;color:#111827;text-decoration:none;margin-bottom:6px}
            .ewp-nav a:hover{background:#F3F4F6}
            .ewp-nav a[aria-current="page"]{background:rgba(44,160,28,0.08);border-left:3px solid #2CA01C;padding-left:8px}
            .ewp-nav .icon{font-size:16px;width:18px;text-align:center}
            .ewp-footer{color:#6B7280;font-size:12px;padding-top:8px}
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Logo/Company Name
        primary_color = branding.get("primary_color", "#4A7C59")
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        if branding.get("logo_url"):
            st.image(branding["logo_url"], width=150)
        else:
            # Default compact logo + company
            st.markdown(f"""
            <div class='ewp-sidebar-logo'>
              <div style="display:flex;align-items:center;gap:10px">
                <div style="width:36px;height:36px;border-radius:8px;background:{primary_color};display:flex;align-items:center;justify-content:center;color:white;font-weight:700">E</div>
                <div>
                  <div class='ewp-company' style='color:{primary_color}'>{company_name}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        
        # User info
                user = st.session_state.get("user", {})
                if user:
                        st.markdown(f"""
                        <div class='ewp-user-pill'>
                            <div style='display:flex;align-items:center;gap:10px'>
                                <div style='width:36px;height:36px;border-radius:8px;background:{primary_color};display:flex;align-items:center;justify-content:center;color:white'>👤</div>
                                <div>
                                    <div style='font-weight:600;color:#111827'>{user.get('name', 'User')}</div>
                                    <div style='color:#6B7280;font-size:12px'>{user.get('role', 'Employee').title()}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation (icons + labels) - keep routing paths intact
        st.markdown("<div class='ewp-nav'>", unsafe_allow_html=True)
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/2_Jobs.py", label="📋 Jobs")
        st.page_link("pages/3_Cost_Entry.py", label="💰 Cost Entry")
        st.page_link("pages/4_Customers.py", label="👥 Customers")
        st.page_link("pages/5_Vendors.py", label="🏪 Vendors")
        st.page_link("pages/6_Reports.py", label="📈 Reports")
        st.page_link("pages/7_Employees.py", label="👷 Employees")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Admin pages
        user_role = user.get("role", "")
        if user_role in ("admin", "super_admin"):
            st.markdown("---")
            st.markdown("**Admin**")
            st.page_link("pages/8_Settings.py", label="⚙️ Settings")
        
        st.markdown("---")
        # Logout (keeps same behavior)
        if st.button("🚪 Logout", use_container_width=True):
            logout()

        st.markdown(f"<div class='ewp-footer'>v2.0 | {company_name}</div>", unsafe_allow_html=True)
