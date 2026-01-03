"""Employees Page - Professional SaaS Colors"""
import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Employees | Elite Wall Pro", page_icon="👷", layout="wide")

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
tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#6366F1", "company_name": "Elite Wall Pro"})
primary_color = branding.get("primary_color", "#6366F1")

# CRITICAL: Apply CSS BEFORE rendering sidebar
st.markdown(get_professional_css(primary_color), unsafe_allow_html=True)

# Additional Employees page-specific CSS
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

    /* ===== Employee Expanders ===== */
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
    .stNumberInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
        font-size: 0.95rem;
    }}

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
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
    <div class='page-title'>👷 Employees</div>
</div>
""", unsafe_allow_html=True)

api = st.session_state.api_client
can_edit = st.session_state.get("user", {}).get("role", "") in ("admin", "super_admin", "manager")

tab1, tab2 = st.tabs(["📋 All Employees", "➕ New Employee"]) if can_edit else st.tabs(["📋 All Employees"])

with tab1:
    try:
        employees = api.get_employees()
        if employees:
            for e in employees:
                name = f"{e.get('first_name', '')} {e.get('last_name', '')}"
                with st.expander(f"{name} - {e.get('role', 'Employee')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {e.get('employee_id', 'N/A')}")
                        st.write(f"**Email:** {e.get('email', 'N/A')}")
                        st.write(f"**Phone:** {e.get('phone', 'N/A')}")
                    with col2:
                        st.write(f"**Department:** {e.get('department', 'N/A')}")
                        st.write(f"**Hire Date:** {e.get('hire_date', 'N/A')}")
                        rate = e.get('hourly_rate')
                        st.write(f"**Rate:** ${float(rate):,.2f}/hr" if rate else "**Rate:** N/A")
        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>👷</div>
                <div class='empty-state-title'>No employees found</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")

if can_edit:
    with tab2:
        with st.form("new_employee"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *")
                last_name = st.text_input("Last Name *")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
            with col2:
                employee_id = st.text_input("Employee ID")
                role = st.text_input("Role/Title")
                department = st.text_input("Department")
                hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=1.0)
            
            if st.form_submit_button("Create Employee", type="primary"):
                if first_name and last_name:
                    try:
                        api.create_employee({
                            "first_name": first_name, "last_name": last_name,
                            "email": email, "phone": phone, "employee_id": employee_id,
                            "role": role, "department": department, "hourly_rate": hourly_rate
                        })
                        st.success("Employee created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("First and Last name are required")