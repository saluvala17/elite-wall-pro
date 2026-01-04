"""Sidebar Component - Professional SaaS Colors (Fixed Navigation)"""
import streamlit as st
from components.auth import logout


def render_sidebar(branding: dict):
    """Render application sidebar with professional SaaS styling - matches app.py"""
    with st.sidebar:
        # Professional SaaS sidebar styles - matches app.py exactly
        st.markdown(
            """
            <style>
            /* ===== Sidebar Base ===== */
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #1E293B 0%, #334155 50%, #475569 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.06);
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
            }}
            
            [data-testid="stSidebar"] > div:first-child {{
                background: transparent;
                padding-top: 0.5rem;
            }}
            
            /* ===== Logo Section ===== */
            .sidebar-logo {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 16px 16px 12px 16px;
                margin: 0;
            }}
            
            .sidebar-logo-icon {{
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
            }}
            
            .sidebar-logo-text {{
                color: #ffffff;
                font-size: 1.2rem;
                font-weight: 700;
                letter-spacing: -0.02em;
            }}
            
            /* ===== User Pill ===== */
            .ewp-user-pill {{
                background: rgba(255, 255, 255, 0.08);
                padding: 12px 14px;
                border-radius: 10px;
                margin: 0 12px 20px 12px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}
            
            .ewp-user-avatar {{
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
            }}
            
            .ewp-user-name {{
                font-weight: 700;
                color: #ffffff;
                font-size: 0.95rem;
                margin-bottom: 2px;
            }}
            
            .ewp-user-role {{
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.8rem;
                text-transform: uppercase;
                font-weight: 600;
                letter-spacing: 0.05em;
            }}
            
            /* ===== Sidebar Navigation Buttons (matches app.py) ===== */
            [data-testid="stSidebar"] .stButton {{
                margin-bottom: 6px;
            }}

            [data-testid="stSidebar"] .stButton > button {{
                width: 100%;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: rgba(255, 255, 255, 0.9);
                text-align: left;
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 0.95rem;
                font-weight: 600;
                transition: all 0.2s ease;
                height: auto;
                min-height: 44px;
                display: flex;
                align-items: center;
                justify-content: flex-start;
                gap: 10px;
            }}

            /* White arrow for navigation */
            [data-testid="stSidebar"] .stButton > button::after {{
                content: '';
                margin-left: auto;
                width: 0;
                height: 0;
                border-top: 4px solid transparent;
                border-bottom: 4px solid transparent;
                border-left: 5px solid rgba(255, 255, 255, 0.4);
                transition: all 0.2s ease;
            }}

            [data-testid="stSidebar"] .stButton > button:hover {{
                background: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.15);
                transform: translateX(2px);
            }}

            [data-testid="stSidebar"] .stButton > button:hover::after {{
                border-left-color: rgba(255, 255, 255, 0.9);
            }}
            
            /* ===== Dividers ===== */
            [data-testid="stSidebar"] hr {{
                margin: 16px 12px;
                border-color: rgba(255, 255, 255, 0.1);
                opacity: 0.6;
            }}
            
            /* ===== Admin Section Title ===== */
            .admin-section-title {{
                color: rgba(255, 255, 255, 0.6);
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                padding: 8px 12px;
                margin-bottom: 6px;
            }}
            
            /* ===== Logout Button (special styling) ===== */
            .logout-section {{
                margin-top: auto;
                padding: 16px 12px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }}

            .logout-section .stButton > button {{
                background: rgba(239, 68, 68, 0.12);
                border-color: rgba(239, 68, 68, 0.2);
                color: #FCA5A5;
            }}

            .logout-section .stButton > button::after {{
                display: none;
            }}

            .logout-section .stButton > button:hover {{
                background: rgba(239, 68, 68, 0.2);
                border-color: rgba(239, 68, 68, 0.3);
                color: #ffffff;
            }}
            
            /* ===== Footer ===== */
            .ewp-footer {{
                color: rgba(255, 255, 255, 0.5);
                font-size: 0.75rem;
                padding: 16px 12px 8px 12px;
                text-align: center;
            }}
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
            # Default professional logo - matches app.py
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
        
        # Navigation - Using st.button() + st.switch_page() like app.py
        if st.button("🏠  Dashboard", key="nav_home", use_container_width=True):
            st.switch_page("app.py")
        
        # if st.button("📊  Analytics", key="nav_analytics", use_container_width=True):
        #     st.switch_page("pages/1_Dashboard.py")
        
        if st.button("📋  Jobs", key="nav_jobs", use_container_width=True):
            st.switch_page("pages/2_Jobs.py")
        
        if st.button("💰  Cost Entry", key="nav_cost", use_container_width=True):
            st.switch_page("pages/3_Cost_Entry.py")
        
        if st.button("👥  Customers", key="nav_customers", use_container_width=True):
            st.switch_page("pages/4_Customers.py")
        
        if st.button("🏢  Vendors", key="nav_vendors", use_container_width=True):
            st.switch_page("pages/5_Vendors.py")
        
        if st.button("📈  Reports", key="nav_reports", use_container_width=True):
            st.switch_page("pages/6_Reports.py")
        
        if st.button("👷  Employees", key="nav_employees", use_container_width=True):
            st.switch_page("pages/7_Employees.py")
        
        # Admin pages
        user_role = user.get("role", "")
        if user_role in ("admin", "super_admin"):
            st.markdown("---")
            st.markdown('<div class="admin-section-title">ADMIN</div>', unsafe_allow_html=True)
            
            if st.button("⚙️  Settings", key="nav_settings", use_container_width=True):
                st.switch_page("pages/8_Settings.py")
        
        # Spacer
        st.markdown('<div style="flex-grow: 1; min-height: 50px;"></div>', unsafe_allow_html=True)
        
        # Logout
        st.markdown('<div class="logout-section">', unsafe_allow_html=True)
        if st.button("🚪  Logout", key="logout_btn", use_container_width=True):
            logout()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"<div class='ewp-footer'>v2.0 | {company_name}</div>", unsafe_allow_html=True)