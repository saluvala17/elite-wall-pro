"""Sidebar Component - Professional SaaS Colors"""
import streamlit as st
from components.auth import logout


def render_sidebar(branding: dict):
    """Render application sidebar with professional SaaS styling"""
    with st.sidebar:
        # Professional SaaS sidebar styles
        st.markdown(
            """
            <style>
            /* ===== Sidebar Base ===== */
            .stSidebar > div {
                background: linear-gradient(180deg, #1E293B 0%, #334155 50%, #475569 100%) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
            }
            
            /* ===== Logo Section ===== */
            .ewp-sidebar-logo {
                padding: 16px 16px 12px 16px;
                margin: 0;
            }
            
            .ewp-logo-container {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .ewp-logo-icon {
                width: 44px;
                height: 44px;
                border-radius: 12px;
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 800;
                font-size: 1.3rem;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            }
            
            .ewp-company {
                font-weight: 700;
                color: #ffffff;
                font-size: 1.2rem;
                letter-spacing: -0.02em;
            }
            
            /* ===== User Pill ===== */
            .ewp-user-pill {
                background: rgba(255, 255, 255, 0.08);
                padding: 12px 14px;
                border-radius: 10px;
                margin: 0 12px 20px 12px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
            
            .ewp-user-avatar {
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.2rem;
                flex-shrink: 0;
            }
            
            .ewp-user-name {
                font-weight: 700;
                color: #ffffff;
                font-size: 0.95rem;
                margin-bottom: 2px;
            }
            
            .ewp-user-role {
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.8rem;
                text-transform: uppercase;
                font-weight: 600;
                letter-spacing: 0.05em;
            }
            
            /* ===== Navigation Links ===== */
            .ewp-nav {
                padding: 0 12px;
            }
            
            /* Override Streamlit page link styles */
            [data-testid="stSidebar"] a {
                display: flex !important;
                align-items: center !important;
                gap: 12px !important;
                padding: 12px 16px !important;
                border-radius: 8px !important;
                color: rgba(255, 255, 255, 0.9) !important;
                text-decoration: none !important;
                margin-bottom: 6px !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                transition: all 0.2s ease !important;
            }
            
            [data-testid="stSidebar"] a:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: rgba(255, 255, 255, 0.15) !important;
                transform: translateX(2px) !important;
            }
            
            [data-testid="stSidebar"] a[aria-current="page"] {
                background: rgba(99, 102, 241, 0.2) !important;
                border-left: 4px solid #6366F1 !important;
                padding-left: 12px !important;
                border-color: rgba(99, 102, 241, 0.4) !important;
                color: #ffffff !important;
            }
            
            /* ===== Dividers ===== */
            [data-testid="stSidebar"] hr {
                margin: 16px 12px !important;
                border-color: rgba(255, 255, 255, 0.1) !important;
                opacity: 0.6 !important;
            }
            
            /* ===== Admin Section ===== */
            [data-testid="stSidebar"] .stMarkdown strong {
                color: rgba(255, 255, 255, 0.6) !important;
                font-size: 0.7rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.12em !important;
                padding: 0 12px !important;
                display: block !important;
                margin-bottom: 8px !important;
            }
            
            /* ===== Logout Button ===== */
            .logout-button-container {
                padding: 0 12px;
                margin-top: 16px;
            }
            
            .logout-button-container .stButton > button {
                width: 100%;
                background: rgba(239, 68, 68, 0.12) !important;
                border: 1px solid rgba(239, 68, 68, 0.2) !important;
                color: #FCA5A5 !important;
                font-weight: 700 !important;
                border-radius: 8px !important;
                padding: 12px 16px !important;
                transition: all 0.2s ease !important;
            }
            
            .logout-button-container .stButton > button:hover {
                background: rgba(239, 68, 68, 0.2) !important;
                border-color: rgba(239, 68, 68, 0.3) !important;
                color: #ffffff !important;
            }
            
            /* ===== Footer ===== */
            .ewp-footer {
                color: rgba(255, 255, 255, 0.5);
                font-size: 0.75rem;
                padding: 16px 12px 8px 12px;
                text-align: center;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                margin-top: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Logo/Company Name
        primary_color = branding.get("primary_color", "#6366F1")
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        if branding.get("logo_url"):
            st.markdown('<div class="ewp-sidebar-logo">', unsafe_allow_html=True)
            st.image(branding["logo_url"], width=150)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Default professional logo
            st.markdown(f"""
            <div class='ewp-sidebar-logo'>
              <div class='ewp-logo-container'>
                <div class='ewp-logo-icon'>🏗️</div>
                <div class='ewp-company'>{company_name}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        
        # User info
        user = st.session_state.get("user", {})
        if user:
            st.markdown(f"""
            <div class='ewp-user-pill'>
                <div style='display:flex;align-items:center;gap:12px'>
                    <div class='ewp-user-avatar'>👤</div>
                    <div>
                        <div class='ewp-user-name'>{user.get('name', 'User')}</div>
                        <div class='ewp-user-role'>{user.get('role', 'Employee').title()}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
        
        # Navigation (unified menu - no sections)
        st.markdown("<div class='ewp-nav'>", unsafe_allow_html=True)
        st.page_link("app.py", label="🏠  Dashboard")
        st.page_link("pages/1_Dashboard.py", label="📊  Analytics")
        st.page_link("pages/2_Jobs.py", label="📋  Jobs")
        st.page_link("pages/3_Cost_Entry.py", label="💰  Cost Entry")
        st.page_link("pages/4_Customers.py", label="👥  Customers")
        st.page_link("pages/5_Vendors.py", label="🏢  Vendors")
        st.page_link("pages/6_Reports.py", label="📈  Reports")
        st.page_link("pages/7_Employees.py", label="👷  Employees")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Admin pages
        user_role = user.get("role", "")
        if user_role in ("admin", "super_admin"):
            st.markdown("---")
            st.markdown("**ADMIN**")
            st.markdown("<div class='ewp-nav'>", unsafe_allow_html=True)
            st.page_link("pages/8_Settings.py", label="⚙️  Settings")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout
        st.markdown('<div class="logout-button-container">', unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True):
            logout()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"<div class='ewp-footer'>v2.0 | {company_name}</div>", unsafe_allow_html=True)