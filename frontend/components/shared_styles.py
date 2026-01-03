"""
Shared CSS Styles for Elite Wall Pro
Import this at the top of every page for consistent styling
"""

def get_professional_css(primary_color: str = "#6366F1") -> str:
    """
    Returns professional SaaS CSS that includes:
    - Color variables
    - Sidebar styling
    - Main content styling
    - Component styling
    """
    return f"""
    <style>
    /* ===== Professional Color Palette ===== */
    :root {{
        /* Primary Colors - Sophisticated Indigo */
        --primary-600: #4F46E5;
        --primary-500: #6366F1;
        --primary-400: #818CF8;
        
        /* Sidebar Colors - Deep Navy/Slate */
        --sidebar-bg-start: #1E293B;
        --sidebar-bg-mid: #334155;
        --sidebar-bg-end: #475569;
        
        /* Neutral Grays - Clean & Modern */
        --gray-50: #F8FAFC;
        --gray-100: #F1F5F9;
        --gray-200: #E2E8F0;
        --gray-300: #CBD5E1;
        --gray-600: #475569;
        --gray-700: #334155;
        --gray-800: #1E293B;
        --gray-900: #0F172A;
        
        /* Semantic Colors */
        --success: #10B981;
        --success-light: #D1FAE5;
        --warning: #F59E0B;
        --warning-light: #FEF3C7;
        --danger: #EF4444;
        --danger-light: #FEE2E2;
    }}
    
    /* ===== Global Foundation ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: var(--gray-50);
        color: var(--gray-900);
    }}

    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1400px !important;
    }}

    /* ===== CRITICAL: SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--sidebar-bg-start) 0%, var(--sidebar-bg-mid) 50%, var(--sidebar-bg-end) 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12) !important;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
        padding-top: 0.5rem !important;
    }}

    /* Sidebar Logo */
    .sidebar-logo {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 16px 12px 16px;
        margin: 0;
    }}

    .sidebar-logo-icon {{
        background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%);
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
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}

    /* Sidebar User Pill */
    .ewp-user-pill {{
        background: rgba(255, 255, 255, 0.08) !important;
        padding: 12px 14px !important;
        border-radius: 10px !important;
        margin: 0 12px 20px 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }}

    .ewp-user-avatar {{
        width: 40px !important;
        height: 40px !important;
        border-radius: 10px !important;
        background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: white !important;
        font-size: 1.2rem !important;
    }}

    .ewp-user-name {{
        font-weight: 700 !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        margin-bottom: 2px !important;
    }}

    .ewp-user-role {{
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
    }}

    /* Sidebar Navigation Buttons */
    [data-testid="stSidebar"] .stButton {{
        margin-bottom: 6px !important;
    }}

    [data-testid="stSidebar"] .stButton > button {{
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
        height: auto !important;
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
    }}

    [data-testid="stSidebar"] .stButton > button::after {{
        content: '' !important;
        margin-left: auto !important;
        width: 0 !important;
        height: 0 !important;
        border-top: 4px solid transparent !important;
        border-bottom: 4px solid transparent !important;
        border-left: 5px solid rgba(255, 255, 255, 0.4) !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        transform: translateX(2px) !important;
    }}

    [data-testid="stSidebar"] .stButton > button:hover::after {{
        border-left-color: rgba(255, 255, 255, 0.9) !important;
    }}

    /* Admin Section */
    .admin-section-title {{
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        padding: 8px 12px !important;
        margin-bottom: 6px !important;
    }}

    /* Logout Section */
    .logout-section {{
        margin-top: auto !important;
        padding: 16px 12px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}

    .logout-section .stButton > button {{
        background: rgba(239, 68, 68, 0.12) !important;
        border-color: rgba(239, 68, 68, 0.2) !important;
        color: #FCA5A5 !important;
    }}

    .logout-section .stButton > button::after {{
        display: none !important;
    }}

    .logout-section .stButton > button:hover {{
        background: rgba(239, 68, 68, 0.2) !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        color: #ffffff !important;
    }}

    /* Footer */
    .ewp-footer {{
        color: rgba(255, 255, 255, 0.5) !important;
        font-size: 0.75rem !important;
        padding: 16px 12px 8px 12px !important;
        text-align: center !important;
    }}

    [data-testid="stSidebar"] hr {{
        margin: 16px 12px !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        opacity: 0.6 !important;
    }}

    /* ===== Page Header ===== */
    .page-header {{
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--gray-200);
    }}

    .page-title {{
        font-size: 2rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }}

    .page-subtitle {{
        font-size: 1rem;
        color: var(--gray-600);
        font-weight: 500;
    }}

    /* ===== Buttons ===== */
    .stButton > button {{
        border-radius: 8px;
        height: 44px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
    }}

    .stButton > button[kind="primary"]:hover {{
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }}

    .stButton > button[kind="secondary"] {{
        background: #ffffff !important;
        border: 1px solid var(--gray-300) !important;
        color: var(--gray-700) !important;
    }}

    .stButton > button[kind="secondary"]:hover {{
        background: var(--gray-50) !important;
        border-color: var(--gray-600) !important;
    }}

    /* ===== Metrics ===== */
    [data-testid="stMetric"] {{
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid var(--gray-200);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }}

    [data-testid="stMetric"]:hover {{
        border-color: {primary_color}40;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
    }}

    [data-testid="stMetric"] label {{
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: var(--gray-600) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--gray-900) !important;
    }}

    /* ===== Responsive ===== */
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
    }}
    </style>
    """