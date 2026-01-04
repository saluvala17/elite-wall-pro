"""Sidebar Component - Fixed Navigation (No Dynamic Keys)"""
import streamlit as st
from components.auth import logout


def render_sidebar(branding: dict):
    """Render application sidebar with consistent navigation - NO page reloads or flickering"""
    
    with st.sidebar:
        # Professional SaaS sidebar styles - matches app.py exactly
        st.markdown(
            """
            <style>
            /* ===== Sidebar Base ===== */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1E293B 0%, #334155 50%, #475569 100%) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12) !important;
            }
            
            [data-testid="stSidebar"] > div:first-child {
                background: transparent !important;
                padding-top: 0.5rem !important;
            }
            
            /* ===== Logo Section ===== */
            .sidebar-logo {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 16px 16px 12px 16px;
                margin: 0;
            }
            
            .sidebar-logo-icon {
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                width: 44px;
                height: 44px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.3rem;
                flex-shrink: 0;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            }
            
            .sidebar-logo-text {
                color: #ffffff !important;
                font-size: 1.2rem !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em !important;
            }
            
            /* ===== User Pill ===== */
            .ewp-user-pill {
                background: rgba(255, 255, 255, 0.08) !important;
                padding: 12px 14px !important;
                border-radius: 10px !important;
                margin: 0 12px 20px 12px !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
            }
            
            .ewp-user-avatar {
                width: 40px !important;
                height: 40px !important;
                border-radius: 10px !important;
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                color: white !important;
                font-size: 1.2rem !important;
            }
            
            .ewp-user-name {
                font-weight: 700 !important;
                color: #ffffff !important;
                font-size: 0.95rem !important;
                margin-bottom: 2px !important;
            }
            
            .ewp-user-role {
                color: rgba(255, 255, 255, 0.7) !important;
                font-size: 0.8rem !important;
                text-transform: uppercase !important;
                font-weight: 600 !important;
                letter-spacing: 0.05em !important;
            }
            
            /* ===== Sidebar Links (Using st.page_link) ===== */
            [data-testid="stSidebar"] a {
                display: block !important;
                width: 100% !important;
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                color: rgba(255, 255, 255, 0.9) !important;
                text-align: left !important;
                padding: 12px 16px !important;
                border-radius: 8px !important;
                font-size: 0.95rem !important;
                font-weight: 600 !important;
                transition: all 0.2s ease !important;
                margin-bottom: 6px !important;
                text-decoration: none !important;
            }

            [data-testid="stSidebar"] a:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: rgba(255, 255, 255, 0.15) !important;
                transform: translateX(2px) !important;
            }

            [data-testid="stSidebar"] a::after {
                content: '' !important;
                float: right !important;
                width: 0 !important;
                height: 0 !important;
                border-top: 4px solid transparent !important;
                border-bottom: 4px solid transparent !important;
                border-left: 5px solid rgba(255, 255, 255, 0.4) !important;
                transition: all 0.2s ease !important;
                margin-top: 4px !important;
            }

            [data-testid="stSidebar"] a:hover::after {
                border-left-color: rgba(255, 255, 255, 0.9) !important;
            }
            
            /* ===== Dividers ===== */
            [data-testid="stSidebar"] hr {
                margin: 16px 12px !important;
                border-color: rgba(255, 255, 255, 0.1) !important;
                opacity: 0.6 !important;
            }
            
            /* ===== Admin Section Title ===== */
            .admin-section-title {
                color: rgba(255, 255, 255, 0.6) !important;
                font-size: 0.7rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.12em !important;
                padding: 8px 12px !important;
                margin-bottom: 6px !important;
            }
            
            /* ===== Logout Button ===== */
            .logout-section {
                margin-top: auto !important;
                padding: 16px 12px !important;
                border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            }

            .logout-section .stButton > button {
                background: rgba(239, 68, 68, 0.12) !important;
                border: 1px solid rgba(239, 68, 68, 0.2) !important;
                color: #FCA5A5 !important;
                width: 100% !important;
                padding: 12px 16px !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: all 0.2s ease !important;
            }

            .logout-section .stButton > button:hover {
                background: rgba(239, 68, 68, 0.2) !important;
                border-color: rgba(239, 68, 68, 0.3) !important;
                color: #ffffff !important;
            }
            
            /* ===== Footer ===== */
            .ewp-footer {
                color: rgba(255, 255, 255, 0.5) !important;
                font-size: 0.75rem !important;
                padding: 16px 12px 8px 12px !important;
                text-align: center !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Logo/Company Name
        primary_color = branding.get("primary_color", "#6366F1")
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        if branding.get("logo_url"):
            st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
            st.image(branding["logo_url"], width=150)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='sidebar-logo'>
                <div class='sidebar-logo-icon'>🏗️</div>
                <span class='sidebar-logo-text'>{company_name}</span>
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
        
        # Navigation - Using st.page_link (NO page reloads, smooth transitions)
        st.page_link("app.py", label="🏠  Dashboard", icon=None)
        st.page_link("pages/1_Dashboard.py", label="📊  Analytics", icon=None)
        st.page_link("pages/2_Jobs.py", label="📋  Jobs", icon=None)
        st.page_link("pages/3_Cost_Entry.py", label="💰  Cost Entry", icon=None)
        st.page_link("pages/4_Customers.py", label="👥  Customers", icon=None)
        st.page_link("pages/5_Vendors.py", label="🏢  Vendors", icon=None)
        st.page_link("pages/6_Reports.py", label="📈  Reports", icon=None)
        st.page_link("pages/7_Employees.py", label="👷  Employees", icon=None)
        
        # Admin pages
        user_role = user.get("role", "")
        if user_role in ("admin", "super_admin"):
            st.markdown("---")
            st.markdown('<div class="admin-section-title">ADMIN</div>', unsafe_allow_html=True)
            st.page_link("pages/8_Settings.py", label="⚙️  Settings", icon=None)
        
        # Spacer
        st.markdown('<div style="flex-grow: 1; min-height: 50px;"></div>', unsafe_allow_html=True)
        
        # Logout
        st.markdown('<div class="logout-section">', unsafe_allow_html=True)
        if st.button("🚪  Logout", key="sidebar_logout", use_container_width=True):
            logout()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"<div class='ewp-footer'>v2.0 | {company_name}</div>", unsafe_allow_html=True)