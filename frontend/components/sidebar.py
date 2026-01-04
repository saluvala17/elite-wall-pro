"""
Sidebar Component - Professional SaaS Colors
FIXED: No flickering, consistent colors across all pages
"""
import streamlit as st
from components.auth import logout


def render_sidebar(branding: dict):
    """
    Render application sidebar with professional SaaS styling
    Uses buttons for navigation (consistent with app.py)
    """
    
    with st.sidebar:
        # Logo/Company Name
        primary_color = branding.get("primary_color", "#6366F1")
        company_name = branding.get("company_name", "Elite Wall Pro")
        
        if branding.get("logo_url"):
            st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
            st.image(branding["logo_url"], width=150)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Default professional logo
            st.markdown(f"""
            <div class='sidebar-logo'>
                <div class='sidebar-logo-icon'>🏗️</div>
                <span class='sidebar-logo-text'>{company_name}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # User info - COMMENTED OUT (not displayed, but we still need the variable)
        user = st.session_state.get("user", {})
        # if user:
        #     st.markdown(f"""
        #     <div class='ewp-user-pill'>
        #         <div style='display:flex;align-items:center;gap:12px'>
        #             <div class='ewp-user-avatar'>👤</div>
        #             <div>
        #                 <div class='ewp-user-name'>{user.get('name', 'User')}</div>
        #                 <div class='ewp-user-role'>{user.get('role', 'Employee').title()}</div>
        #             </div>
        #         </div>
        #     </div>
        #     """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
        
        # Navigation - Using st.button (consistent with app.py)
        # CRITICAL: Use unique but STABLE keys (not time-based)
        if st.button("🏠  Dashboard", key="nav_dashboard", use_container_width=True):
            st.switch_page("app.py")
        
        # Analytics removed - no longer needed
        # if st.button("📊  Analytics", key="nav_analytics", use_container_width=True):
        #     st.switch_page("pages/1_Dashboard.py")
        
        if st.button("📋  Jobs", key="nav_jobs", use_container_width=True):
            st.switch_page("pages/2_Jobs.py")
        
        if st.button("💰  Cost Entry", key="nav_cost_entry", use_container_width=True):
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
        if st.button("🚪  Logout", key="nav_logout", use_container_width=True):
            logout()
        st.markdown('</div>', unsafe_allow_html=True)

        # Footer
        st.markdown(f"<div class='ewp-footer'>v2.0 | {company_name}</div>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        .ewp-footer {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.75rem;
            padding: 16px 12px 8px 12px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)