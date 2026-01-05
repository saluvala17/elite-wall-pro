"""Customers Page - Professional SaaS Colors"""
import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Customers | Elite Wall Pro", page_icon="👥", layout="wide")

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

# Additional Customers page-specific CSS
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

    /* ===== Customer Expanders ===== */
    .streamlit-expanderHeader {{
        background: #ffffff;
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 16px 20px !important;
        font-weight: 600;
        color: var(--gray-900);
        transition: all 0.2s ease;
    }}

    .streamlit-expanderHeader:hover {{
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        transform: translateY(-1px);
    }}

    div[data-testid="stExpander"] {{
        background: transparent;
        border: none;
        margin-bottom: 12px;
    }}

    .streamlit-expanderContent {{
        background: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
    }}

    /* ===== Input Fields ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
        font-size: 0.95rem;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--primary-500);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }}

    /* ===== Empty State ===== */
    .empty-state {{
        text-align: center;
        padding: 60px 30px;
        background: #ffffff;
        border-radius: 12px;
        border: 2px dashed var(--gray-300);
    }}

    .empty-state-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }}

    .empty-state-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 0.5rem;
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
    <div class='page-title'>👥 Customers</div>
</div>
""", unsafe_allow_html=True)

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
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>👥</div>
                <div class='empty-state-title'>No customers found</div>
            </div>
            """, unsafe_allow_html=True)
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