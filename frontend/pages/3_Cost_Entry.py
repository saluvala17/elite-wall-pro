"""Cost Entry Page with Receipt Scanner"""
import streamlit as st
import base64
from datetime import date, timedelta

st.set_page_config(page_title="Cost Entry | Elite Wall Pro", page_icon="💰", layout="wide")

if not st.session_state.get("authenticated"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar

tenant = st.session_state.get("tenant", {})
branding = tenant.get("branding", {"primary_color": "#4A7C59", "company_name": "Elite Wall Pro"})
render_sidebar(branding)

st.title("💰 Weekly Cost Entry")

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
    st.error(f"Failed to load jobs: {e}")
    jobs = []

if not jobs:
    st.info("No active jobs found. Create an active job first.")
    st.stop()

# Job selection
job_options = {f"{j.get('job_number')} - {j.get('job_name')}": j for j in jobs}
selected_job_name = st.selectbox("Select Job", list(job_options.keys()))
selected_job = job_options[selected_job_name]

# Week selection
week_endings = get_week_endings()
week_options = [w.strftime('%Y-%m-%d') + f" ({w.strftime('%b %d')})" for w in week_endings]
selected_week_display = st.selectbox("Week Ending (Saturday)", week_options)
selected_week = selected_week_display.split(" ")[0]

st.markdown("---")

# Tabs
entry_tab, scanner_tab, history_tab = st.tabs(["✏️ Manual Entry", "📸 Scan Receipt", "📊 History"])

# ==========================================
# MANUAL ENTRY TAB
# ==========================================
with entry_tab:
    st.subheader(f"Enter Costs for Week Ending {selected_week}")
    
    # Get existing entry
    try:
        existing_costs = api.get_weekly_costs(selected_job["id"])
        existing_entry = next((c for c in existing_costs if c.get("week_ending") == selected_week), None)
    except:
        existing_entry = None
    
    # Check if receipt was applied
    applied_totals = st.session_state.get("receipt_category_totals", {})
    if applied_totals:
        st.success(f"✅ Receipt applied! Total: ${sum(applied_totals.values()):,.2f}")
        with st.expander("Category Breakdown"):
            for cat, amt in applied_totals.items():
                if amt > 0:
                    st.write(f"• {cat.replace('_', ' ').title()}: ${amt:,.2f}")
    
    with st.form("cost_entry"):
        col1, col2, col3 = st.columns(3)
        
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
        
        with col1:
            insurance = st.number_input("Insurance ($)", min_value=0.0, value=insurance, step=100.0)
            labor = st.number_input("Labor ($)", min_value=0.0, value=labor, step=100.0)
        
        with col2:
            stamps = st.number_input("Stamps ($)", min_value=0.0, value=stamps, step=100.0)
            material = st.number_input("Material ($)", min_value=0.0, value=material, step=100.0)
        
        with col3:
            subs_bond = st.number_input("Subs & Bond ($)", min_value=0.0, value=subs_bond, step=100.0)
            equipment = st.number_input("Equipment ($)", min_value=0.0, value=equipment, step=100.0)
        
        man_days = st.number_input("Man Days", min_value=0, 
                                   value=int(existing_entry.get("man_days_actual", 0) if existing_entry else 0))
        notes = st.text_area("Notes", value=existing_entry.get("notes", "") if existing_entry else "")
        
        if st.form_submit_button("💾 Save Costs", use_container_width=True, type="primary"):
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
                st.success("✅ Costs saved!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save: {e}")


# ==========================================
# RECEIPT SCANNER TAB
# ==========================================
with scanner_tab:
    st.subheader("📸 Scan Receipt")
    
    # Check if scanning is available
    try:
        scan_status = api.get_receipt_status()
        scanning_available = scan_status.get("available", False)
    except:
        scanning_available = False
    
    if not scanning_available:
        st.warning("⚠️ Receipt scanning requires Anthropic API key configuration on the server.")
    
    uploaded_file = st.file_uploader(
        "Upload receipt image",
        type=["jpg", "jpeg", "png", "gif", "webp", "pdf"]
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, width=300)
        
        with col2:
            if st.button("🔍 Scan Receipt", type="primary", disabled=not scanning_available):
                with st.spinner("Analyzing receipt..."):
                    try:
                        uploaded_file.seek(0)
                        content = uploaded_file.read()
                        image_b64 = base64.b64encode(content).decode("utf-8")
                        data_uri = f"data:{uploaded_file.type};base64,{image_b64}"
                        
                        result = api.scan_receipt(data_uri, selected_job.get("job_name", ""))
                        st.session_state.scanned_receipt = result
                        st.success("✅ Receipt scanned!")
                    except Exception as e:
                        st.error(f"Scan failed: {e}")
    
    # Show scanned results
    if "scanned_receipt" in st.session_state:
        receipt = st.session_state.scanned_receipt
        
        st.markdown("---")
        st.subheader("📋 Extracted Data")
        
        confidence = receipt.get("confidence_score", 0)
        if confidence >= 0.8:
            st.success(f"High confidence: {confidence:.0%}")
        else:
            st.warning(f"Medium confidence: {confidence:.0%} - Please verify")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Vendor:** {receipt.get('vendor_name', 'Unknown')}")
            st.write(f"**Date:** {receipt.get('receipt_date', 'N/A')}")
        with col2:
            st.write(f"**Total:** ${receipt.get('total', 0):,.2f}")
        
        # Line items with categories
        line_items = receipt.get("line_items", [])
        if line_items:
            st.markdown("### Line Items")
            
            categories = ["material", "subs_bond", "labor", "equipment", "insurance", "stamps"]
            category_totals = {cat: 0.0 for cat in categories}
            
            for i, item in enumerate(line_items):
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    desc = item.get("description", item.get("vendor_name", "Item"))
                    st.write(desc[:50])
                
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
                    st.write(f"${amt:,.2f}")
                    category_totals[new_cat] += amt
            
            st.markdown("### Category Totals")
            cols = st.columns(3)
            for i, (cat, amt) in enumerate(category_totals.items()):
                if amt > 0:
                    with cols[i % 3]:
                        st.metric(cat.replace("_", " ").title(), f"${amt:,.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Apply to Cost Entry", type="primary", use_container_width=True):
                st.session_state.receipt_category_totals = category_totals
                del st.session_state.scanned_receipt
                st.success("Applied! Go to Manual Entry tab to save.")
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                del st.session_state.scanned_receipt
                st.rerun()


# ==========================================
# HISTORY TAB
# ==========================================
with history_tab:
    st.subheader("📊 Cost History")
    
    try:
        costs = api.get_weekly_costs(selected_job["id"])
        
        if costs:
            for cost in costs[:10]:
                with st.expander(f"Week: {cost.get('week_ending', 'N/A')}"):
                    total = sum([
                        float(cost.get("insurance_actual", 0) or 0),
                        float(cost.get("labor_actual", 0) or 0),
                        float(cost.get("stamps_actual", 0) or 0),
                        float(cost.get("material_actual", 0) or 0),
                        float(cost.get("subs_bond_actual", 0) or 0),
                        float(cost.get("equipment_actual", 0) or 0),
                    ])
                    st.write(f"**Total:** ${total:,.2f}")
                    st.write(f"Man Days: {cost.get('man_days_actual', 0)}")
        else:
            st.info("No cost entries yet")
    except Exception as e:
        st.error(f"Error loading history: {e}")
