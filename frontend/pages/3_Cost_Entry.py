"""Cost Entry Page with Receipt Scanner - Professional SaaS Colors"""
import streamlit as st
import base64
from datetime import date, timedelta
import sys
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Cost Entry | Elite Wall Pro", page_icon="💰", layout="wide")

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

# Additional Cost Entry page-specific CSS
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

    /* ===== Select Boxes ===== */
    .stSelectbox > div > div {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        background: #ffffff;
    }}

    /* ===== Success Banner ===== */
    .success-banner {{
        background: linear-gradient(135deg, var(--success-light) 0%, #D1FAE5 100%);
        border: 1px solid #86efac;
        border-left: 4px solid var(--success);
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.1);
    }}

    .success-icon {{
        font-size: 1.5rem;
    }}

    .success-text {{
        flex: 1;
    }}

    .success-title {{
        font-weight: 600;
        color: var(--success);
        margin-bottom: 4px;
    }}

    .success-details {{
        font-size: 0.875rem;
        color: var(--success);
    }}

    /* ===== Form Sections ===== */
    .form-section {{
        background: #ffffff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }}

    .form-section-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--gray-200);
    }}

    /* ===== Number Inputs ===== */
    .stNumberInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
        background: #ffffff;
    }}

    .stNumberInput > div > div > input:focus {{
        border-color: {primary_color};
        box-shadow: 0 0 0 3px {primary_color}20;
    }}

    /* ===== Text Areas ===== */
    .stTextArea > div > div > textarea {{
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        padding: 12px 16px;
        background: #ffffff;
    }}

    /* ===== Buttons ===== */
    .stButton > button {{
        border-radius: 8px;
        height: 44px;
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}

    .stButton > button[kind="primary"] {{
        background: {primary_color} !important;
        border-color: {primary_color} !important;
    }}

    /* ===== File Uploader ===== */
    .uploadedFile {{
        background: #ffffff;
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        padding: 12px;
    }}

    /* ===== Receipt Preview ===== */
    .receipt-preview {{
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }}

    /* ===== Scanned Data Card ===== */
    .scanned-data-card {{
        background: var(--gray-50);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        margin-top: 20px;
    }}

    .confidence-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
    }}

    .confidence-high {{
        background: var(--success-light);
        color: var(--success);
    }}

    .confidence-medium {{
        background: var(--warning-light);
        color: var(--warning);
    }}

    /* ===== Line Item Row ===== */
    .line-item-row {{
        background: #ffffff;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        margin-bottom: 10px;
        display: grid;
        grid-template-columns: 2fr 1.5fr 0.5fr;
        gap: 16px;
        align-items: center;
    }}

    .item-description {{
        color: var(--gray-900);
        font-weight: 500;
    }}

    .item-amount {{
        color: var(--gray-900);
        font-weight: 600;
        text-align: right;
    }}

    /* ===== Category Totals ===== */
    .category-total {{
        background: #ffffff;
        padding: 16px 20px;
        border-radius: 8px;
        border: 1px solid var(--gray-200);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .category-label {{
        color: var(--gray-600);
        font-weight: 500;
        text-transform: capitalize;
    }}

    .category-value {{
        color: var(--gray-900);
        font-weight: 700;
        font-size: 1.1rem;
    }}

    /* ===== Warning Box ===== */
    .warning-box {{
        background: var(--warning-light);
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 10px;
        display: flex;
        align-items: start;
        gap: 12px;
    }}

    .warning-icon {{
        font-size: 1.5rem;
    }}

    .warning-text {{
        color: #92400e;
    }}

    /* ===== History Expander ===== */
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

    /* ===== Info Messages ===== */
    .stAlert {{
        border-radius: 10px;
        border-left-width: 4px;
    }}

    /* ===== Responsive ===== */
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        
        .line-item-row {{
            grid-template-columns: 1fr;
        }}
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
    <div class='page-title'>💰 Cost Entry</div>
</div>
""", unsafe_allow_html=True)

api = st.session_state.api_client


def get_week_endings(n=12):
    """Get last n week ending dates (Saturdays)"""
    today = date.today()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0 and today.weekday() != 5:
        days_until_saturday = 7
    next_saturday = today + timedelta(days=days_until_saturday)
    return [next_saturday - timedelta(weeks=i) for i in range(n)]


# Load jobs
try:
    jobs = api.get_jobs(status="active")
except Exception as e:
    st.error(f"⚠️ Failed to load jobs: {e}")
    jobs = []

if not jobs:
    st.info("ℹ️ No active jobs found. Create an active job first.")
    if st.button("➕ Create Job", type="primary"):
        st.switch_page("pages/2_Jobs.py")
    st.stop()

# Job & Week Selection
col1, col2 = st.columns(2)

with col1:
    job_options = {f"{j.get('job_number')} - {j.get('job_name')}": j for j in jobs}
    selected_job_name = st.selectbox("📋 Select Job", list(job_options.keys()))
    selected_job = job_options[selected_job_name]

with col2:
    week_endings = get_week_endings()
    week_options = [w.strftime('%Y-%m-%d') + f" ({w.strftime('%b %d')})" for w in week_endings]
    selected_week_display = st.selectbox("📅 Week Ending (Saturday)", week_options)
    selected_week = selected_week_display.split(" ")[0]

st.write("")

# Tabs
entry_tab, scanner_tab, history_tab = st.tabs(["✏️ Manual Entry", "📸 Scan Receipt", "📊 History"])

# ==========================================
# MANUAL ENTRY TAB
# ==========================================
with entry_tab:
    st.markdown(f'<div class="form-section-title">Enter Costs for Week Ending {selected_week}</div>', unsafe_allow_html=True)
    
    # Get existing entry
    try:
        existing_costs = api.get_weekly_costs(selected_job["id"])
        existing_entry = next((c for c in existing_costs if c.get("week_ending") == selected_week), None)
    except:
        existing_entry = None
    
    # Check if receipt was applied
    applied_totals = st.session_state.get("receipt_category_totals", {})
    if applied_totals:
        total_applied = sum(applied_totals.values())
        st.markdown(f"""
        <div class='success-banner'>
            <div class='success-icon'>✅</div>
            <div class='success-text'>
                <div class='success-title'>Receipt Applied Successfully</div>
                <div class='success-details'>Total: ${total_applied:,.2f} distributed across categories</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 Category Breakdown", expanded=False):
            for cat, amt in applied_totals.items():
                if amt > 0:
                    st.markdown(f"""
                    <div class='category-total'>
                        <span class='category-label'>{cat.replace('_', ' ').title()}</span>
                        <span class='category-value'>${amt:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    with st.form("cost_entry"):
        base_insurance = float(existing_entry.get("insurance_actual", 0) if existing_entry else 0)
        base_labor = float(existing_entry.get("labor_actual", 0) if existing_entry else 0)
        base_stamps = float(existing_entry.get("stamps_actual", 0) if existing_entry else 0)
        base_material = float(existing_entry.get("material_actual", 0) if existing_entry else 0)
        base_subs = float(existing_entry.get("subs_bond_actual", 0) if existing_entry else 0)
        base_equipment = float(existing_entry.get("equipment_actual", 0) if existing_entry else 0)
        
        # Add receipt amounts
        insurance = base_insurance + applied_totals.get("insurance", 0)
        labor = base_labor + applied_totals.get("labor", 0)
        stamps = base_stamps + applied_totals.get("stamps", 0)
        material = base_material + applied_totals.get("material", 0)
        subs_bond = base_subs + applied_totals.get("subs_bond", 0)
        equipment = base_equipment + applied_totals.get("equipment", 0)
        
        st.markdown("### 💵 Cost Categories")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            insurance = st.number_input("🛡️ Insurance ($)", min_value=0.0, value=insurance, step=100.0, format="%.2f")
            labor = st.number_input("👷 Labor ($)", min_value=0.0, value=labor, step=100.0, format="%.2f")
        
        with col2:
            stamps = st.number_input("📮 Stamps ($)", min_value=0.0, value=stamps, step=100.0, format="%.2f")
            material = st.number_input("🧱 Material ($)", min_value=0.0, value=material, step=100.0, format="%.2f")
        
        with col3:
            subs_bond = st.number_input("🤝 Subs & Bond ($)", min_value=0.0, value=subs_bond, step=100.0, format="%.2f")
            equipment = st.number_input("🚜 Equipment ($)", min_value=0.0, value=equipment, step=100.0, format="%.2f")
        
        st.write("")
        
        # Totals
        total_costs = insurance + labor + stamps + material + subs_bond + equipment
        st.markdown(f"""
        <div class='category-total' style='background: #f0fdf4; border-color: #86efac;'>
            <span class='category-label' style='color: var(--success);'>Total Weekly Costs</span>
            <span class='category-value' style='color: var(--success);'>${total_costs:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("### 📋 Additional Details")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            man_days = st.number_input("👥 Man Days", min_value=0, 
                                       value=int(existing_entry.get("man_days_actual", 0) if existing_entry else 0))
        
        notes = st.text_area("📝 Notes", value=existing_entry.get("notes", "") if existing_entry else "",
                            placeholder="Add any relevant notes or comments...", height=100)
        
        st.write("")
        
        # Submit
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("💾 Save Costs", use_container_width=True, type="primary")
        
        if submit:
            cost_data = {
                "job_id": selected_job["id"],
                "week_ending": selected_week,
                "insurance_actual": insurance,
                "labor_actual": labor,
                "stamps_actual": stamps,
                "material_actual": material,
                "subs_bond_actual": subs_bond,
                "equipment_actual": equipment,
                "man_days_actual": man_days,
                "notes": notes
            }
            
            try:
                api.save_weekly_cost(cost_data)
                st.session_state.receipt_category_totals = {}  # Clear
                st.success("✅ Costs saved successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to save: {e}")


# ==========================================
# RECEIPT SCANNER TAB
# ==========================================
with scanner_tab:
    st.markdown('<div class="form-section-title">📸 Scan Receipt</div>', unsafe_allow_html=True)
    
    # Check if scanning is available
    try:
        scan_status = api.get_receipt_status()
        scanning_available = scan_status.get("available", False)
    except:
        scanning_available = False
    
    if not scanning_available:
        st.markdown("""
        <div class='warning-box'>
            <div class='warning-icon'>⚠️</div>
            <div class='warning-text'>
                <strong>Receipt scanning unavailable</strong><br>
                Anthropic API key configuration required on the server.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📁 Upload receipt image",
            type=["jpg", "jpeg", "png", "gif", "webp", "pdf"],
            help="Supported formats: JPG, PNG, GIF, WebP, PDF"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Receipt Preview", use_container_width=True)
    
    with col2:
        if uploaded_file:
            st.write("")
            st.write("")
            if st.button("🔍 Scan Receipt", type="primary", disabled=not scanning_available, use_container_width=True):
                with st.spinner("🔄 Analyzing receipt..."):
                    try:
                        uploaded_file.seek(0)
                        content = uploaded_file.read()
                        image_b64 = base64.b64encode(content).decode("utf-8")
                        data_uri = f"data:{uploaded_file.type};base64,{image_b64}"
                        
                        result = api.scan_receipt(data_uri, selected_job.get("job_name", ""))
                        st.session_state.scanned_receipt = result
                        st.success("✅ Receipt scanned successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Scan failed: {e}")
    
    # Show scanned results
    if "scanned_receipt" in st.session_state:
        receipt = st.session_state.scanned_receipt
        
        st.markdown("---")
        st.markdown('<div class="form-section-title">📋 Extracted Data</div>', unsafe_allow_html=True)
        
        # Confidence
        confidence = receipt.get("confidence_score", 0)
        confidence_class = "confidence-high" if confidence >= 0.8 else "confidence-medium"
        confidence_text = "High Confidence" if confidence >= 0.8 else "Medium Confidence - Please Verify"
        
        st.markdown(f"""
        <div class='confidence-badge {confidence_class}'>
            {confidence_text}: {confidence:.0%}
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Receipt Info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Vendor:** {receipt.get('vendor_name', 'Unknown')}")
            st.markdown(f"**Date:** {receipt.get('receipt_date', 'N/A')}")
        with col2:
            st.markdown(f"**Total:** ${receipt.get('total', 0):,.2f}")
        
        st.write("")
        
        # Line items with categories
        line_items = receipt.get("line_items", [])
        if line_items:
            st.markdown("### 📝 Line Items")
            
            categories = ["material", "subs_bond", "labor", "equipment", "insurance", "stamps"]
            category_totals = {cat: 0.0 for cat in categories}
            
            for i, item in enumerate(line_items):
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    desc = item.get("description", item.get("vendor_name", "Item"))
                    st.markdown(f'<div class="item-description">{desc[:50]}</div>', unsafe_allow_html=True)
                
                with col2:
                    current_cat = item.get("category", "material")
                    new_cat = st.selectbox(
                        "Category",
                        categories,
                        index=categories.index(current_cat) if current_cat in categories else 0,
                        key=f"cat_{i}",
                        label_visibility="collapsed"
                    )
                    item["category"] = new_cat
                
                with col3:
                    amt = float(item.get("total", item.get("amount", 0)) or 0)
                    st.markdown(f'<div class="item-amount">${amt:,.2f}</div>', unsafe_allow_html=True)
                    category_totals[new_cat] += amt
            
            st.write("")
            st.markdown("### 💰 Category Totals")
            
            for cat, amt in category_totals.items():
                if amt > 0:
                    st.markdown(f"""
                    <div class='category-total'>
                        <span class='category-label'>{cat.replace("_", " ").title()}</span>
                        <span class='category-value'>${amt:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.write("")
        
        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Apply to Cost Entry", type="primary", use_container_width=True):
                st.session_state.receipt_category_totals = category_totals
                del st.session_state.scanned_receipt
                st.success("✅ Applied! Go to Manual Entry tab to save.")
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                del st.session_state.scanned_receipt
                st.rerun()


# ==========================================
# HISTORY TAB
# ==========================================
with history_tab:
    st.markdown('<div class="form-section-title">📊 Cost History</div>', unsafe_allow_html=True)
    
    try:
        costs = api.get_weekly_costs(selected_job["id"])
        
        if costs:
            for cost in costs[:10]:
                week = cost.get('week_ending', 'N/A')
                total = sum([
                    float(cost.get("insurance_actual", 0) or 0),
                    float(cost.get("labor_actual", 0) or 0),
                    float(cost.get("stamps_actual", 0) or 0),
                    float(cost.get("material_actual", 0) or 0),
                    float(cost.get("subs_bond_actual", 0) or 0),
                    float(cost.get("equipment_actual", 0) or 0),
                ])
                
                with st.expander(f"📅 Week: {week} - Total: ${total:,.2f}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**Insurance:** ${float(cost.get('insurance_actual', 0) or 0):,.2f}")
                        st.markdown(f"**Labor:** ${float(cost.get('labor_actual', 0) or 0):,.2f}")
                    
                    with col2:
                        st.markdown(f"**Stamps:** ${float(cost.get('stamps_actual', 0) or 0):,.2f}")
                        st.markdown(f"**Material:** ${float(cost.get('material_actual', 0) or 0):,.2f}")
                    
                    with col3:
                        st.markdown(f"**Subs & Bond:** ${float(cost.get('subs_bond_actual', 0) or 0):,.2f}")
                        st.markdown(f"**Equipment:** ${float(cost.get('equipment_actual', 0) or 0):,.2f}")
                    
                    st.write("")
                    st.markdown(f"**Man Days:** {cost.get('man_days_actual', 0)}")
                    
                    if cost.get('notes'):
                        st.markdown(f"**Notes:** {cost.get('notes')}")
        else:
            st.info("📭 No cost entries yet for this job")
    
    except Exception as e:
        st.error(f"⚠️ Error loading history: {e}")