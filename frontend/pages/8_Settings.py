"""Settings Page - Professional SaaS Colors"""
import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Settings | Elite Wall Pro", page_icon="⚙️", layout="wide")

# CRITICAL: Hide Streamlit defaults FIRST
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

# Import shared styles and sidebar
from components.shared_styles import get_professional_css
from components.sidebar import render_sidebar

# Get branding
tenant = st.session_state.get("tenant") or {}
branding = tenant.get("branding", {"primary_color": "#6366F1", "company_name": "Elite Wall Pro"})
primary_color = branding.get("primary_color", "#6366F1")

# CRITICAL: Apply CSS BEFORE rendering sidebar
st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)

# Additional Settings page-specific CSS
st.markdown(
    f"""
    <style>
    /* ===== Tabs Enhancement ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 44px;
        padding: 0 24px;
        background-color: transparent;
        border-radius: 6px;
        color: var(--gray-600);
        font-weight: 600;
        border: none;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: var(--primary-500) !important;
        color: #ffffff !important;
    }}

    /* ===== Subheaders ===== */
    h3 {{
        color: var(--gray-900) !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }}

    /* ===== Input Fields ===== */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
        font-size: 0.95rem;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: var(--primary-500);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }}

    /* ===== Color Picker ===== */
    .stColorPicker > div > div {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# NOW render sidebar (after all CSS is loaded)
render_sidebar(branding)

# Header
st.markdown("""
<div class='page-header'>
    <div class='page-title'>⚙️ Settings</div>
</div>
""", unsafe_allow_html=True)

# Admin check
user = st.session_state.get("user", {})
if user.get("role") not in ("admin", "super_admin"):
    st.error("Admin access required")
    st.stop()

api = st.session_state.api_client

tab1, tab2, tab3 = st.tabs(["🎨 Branding", "👥 Users", "🔧 System"])

with tab1:
    st.subheader("Company Branding")
    
    current_branding = branding
    
    with st.form("branding_form"):
        company_name = st.text_input("Company Name", value=current_branding.get("company_name", ""))
        primary_color = st.color_picker("Primary Color", value=current_branding.get("primary_color", "#6366F1"))
        secondary_color = st.color_picker("Secondary Color", value=current_branding.get("secondary_color", "#4F46E5"))
        logo_url = st.text_input("Logo URL", value=current_branding.get("logo_url", "") or "")
        
        if st.form_submit_button("Save Branding", type="primary"):
            try:
                api.update_tenant_branding({
                    "company_name": company_name,
                    "primary_color": primary_color,
                    "secondary_color": secondary_color,
                    "logo_url": logo_url or None
                })
                
                # Update session
                if st.session_state.tenant:
                    st.session_state.tenant["branding"] = {
                        "company_name": company_name,
                        "primary_color": primary_color,
                        "secondary_color": secondary_color,
                        "logo_url": logo_url
                    }
                
                st.success("Branding updated!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save: {e}")

with tab2:
    st.subheader("User Management")
    st.info("User management is handled through Supabase Authentication dashboard.")
    st.markdown("""
    To manage users:
    1. Go to your Supabase dashboard
    2. Navigate to Authentication → Users
    3. Invite new users or manage existing ones
    
    Users will automatically be assigned to your organization when they sign up with your organization code.
    """)

with tab3:
    st.subheader("System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Application Version:** 2.0.0")
        st.write("**Tenant ID:**", tenant.get("id", "N/A")[:8] + "..." if tenant.get("id") else "N/A")
        st.write("**Subdomain:**", tenant.get("subdomain", "N/A"))
    
    with col2:
        st.write("**Subscription:**", tenant.get("subscription_tier", "basic").title())
        st.write("**Status:**", tenant.get("subscription_status", "active").title())
    
    st.markdown("---")
    
    # Receipt scanning status
    try:
        scan_status = api.get_receipt_status()
        if scan_status.get("available"):
            st.success("✅ Receipt Scanning: Available")
        else:
            st.warning("⚠️ Receipt Scanning: Not configured")
    except:
        st.warning("⚠️ Receipt Scanning: Status unknown")