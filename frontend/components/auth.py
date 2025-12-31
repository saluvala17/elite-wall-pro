"""Authentication Components"""
import streamlit as st
from api_client import APIClient


def check_auth() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)


def logout():
    """Log out user"""
    api = st.session_state.get("api_client")
    if api:
        api.signout()
    
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.tenant = None
    st.session_state.access_token = None
    st.rerun()


def render_login_page():
    """Render login page"""
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 4rem auto;
            padding: 2rem;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🏗️ Elite Wall Pro")
        st.markdown("### Sign In")
        
        # Tabs for login/signup
        login_tab, signup_tab = st.tabs(["Sign In", "Create Account"])
        
        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
                    if not email or not password:
                        st.error("Please enter email and password")
                    else:
                        try:
                            api: APIClient = st.session_state.api_client
                            result = api.signin(email, password)
                            
                            if result:
                                st.session_state.authenticated = True
                                st.session_state.user = result.get("user")
                                
                                # Load tenant info
                                try:
                                    tenant = api.get_tenant()
                                    st.session_state.tenant = tenant
                                except:
                                    pass
                                
                                st.success("Signed in successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Sign in failed: {e}")
        
        with signup_tab:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email_signup = st.text_input("Email", key="signup_email")
                password_signup = st.text_input("Password", type="password", key="signup_password")
                password_confirm = st.text_input("Confirm Password", type="password")
                tenant_subdomain = st.text_input(
                    "Organization Code",
                    help="Enter the code provided by your organization"
                )
                
                if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
                    if not all([name, email_signup, password_signup, tenant_subdomain]):
                        st.error("Please fill in all fields")
                    elif password_signup != password_confirm:
                        st.error("Passwords do not match")
                    elif len(password_signup) < 8:
                        st.error("Password must be at least 8 characters")
                    else:
                        try:
                            api: APIClient = st.session_state.api_client
                            result = api.signup(
                                email_signup,
                                password_signup,
                                name,
                                tenant_subdomain
                            )
                            
                            if result:
                                st.session_state.authenticated = True
                                st.session_state.user = result.get("user")
                                st.success("Account created successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Sign up failed: {e}")
        
        st.markdown("---")
        st.caption("Powered by Forge N Systems")
