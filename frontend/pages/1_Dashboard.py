import streamlit as st
from datetime import datetime
from frontend.api_client import get_recent_jobs, get_recent_receipts, get_recent_customers, get_recent_vendors

# Set page configuration
st.set_page_config(
    page_title="Elite Wall Pro - Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define custom CSS styles
st.markdown(
    """
    <style>
    .container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-gap: 20px;
    }
    .card {
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }
    .card-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-content {
        font-size: 14px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fetch data from API
recent_jobs = get_recent_jobs()
recent_receipts = get_recent_receipts()
recent_customers = get_recent_customers()
recent_vendors = get_recent_vendors()

# Render the dashboard
st.title("Dashboard")

with st.container():
    # Recent Jobs
    with st.container():
        st.markdown(
            f"""
            <div class="card">
                <div class="card-header">Recent Jobs</div>
                <div class="card-content">
                    {len(recent_jobs)} recent jobs
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Recent Receipts
    with st.container():
        st.markdown(
            f"""
            <div class="card">
                <div class="card-header">Recent Receipts</div>
                <div class="card-content">
                    {len(recent_receipts)} recent receipts
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.container():
    # Recent Customers
    with st.container():
        st.markdown(
            f"""
            <div class="card">
                <div class="card-header">Recent Customers</div>
                <div class="card-content">
                    {len(recent_customers)} recent customers
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Recent Vendors
    with st.container():
        st.markdown(
            f"""
            <div class="card">
                <div class="card-header">Recent Vendors</div>
                <div class="card-content">
                    {len(recent_vendors)} recent vendors
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
