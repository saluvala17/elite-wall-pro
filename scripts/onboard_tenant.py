#!/usr/bin/env python3
"""
Elite Wall Pro - Tenant Onboarding Script
Creates a new tenant with admin user

Usage:
    python onboard_tenant.py --name "Acme Construction" --subdomain "acme" --admin-email "admin@acme.com"
"""
import argparse
import os
import sys
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from supabase import create_client
    from dotenv import load_dotenv
except ImportError:
    print("Please install required packages: pip install supabase python-dotenv")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Onboard a new tenant")
    parser.add_argument("--name", required=True, help="Company name")
    parser.add_argument("--subdomain", required=True, help="Unique subdomain/code")
    parser.add_argument("--admin-email", required=True, help="Admin user email")
    parser.add_argument("--admin-name", help="Admin user name (defaults to 'Admin')")
    parser.add_argument("--primary-color", default="#4A7C59", help="Primary brand color")
    parser.add_argument("--tier", default="basic", choices=["basic", "professional", "enterprise"])
    
    args = parser.parse_args()
    
    # Load environment
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not service_key:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
        sys.exit(1)
    
    # Get admin password
    admin_password = getpass("Enter admin password (min 8 chars): ")
    if len(admin_password) < 8:
        print("Error: Password must be at least 8 characters")
        sys.exit(1)
    
    confirm_password = getpass("Confirm password: ")
    if admin_password != confirm_password:
        print("Error: Passwords do not match")
        sys.exit(1)
    
    print(f"\nOnboarding new tenant: {args.name}")
    print(f"Subdomain: {args.subdomain}")
    print(f"Admin email: {args.admin_email}")
    print()
    
    # Create Supabase client with service role
    supabase = create_client(supabase_url, service_key)
    
    try:
        # 1. Check if subdomain exists
        existing = supabase.table("tenants").select("id").eq("subdomain", args.subdomain).execute()
        if existing.data:
            print(f"Error: Subdomain '{args.subdomain}' already exists")
            sys.exit(1)
        
        # 2. Create tenant
        print("Creating tenant...")
        tenant_data = {
            "name": args.name,
            "subdomain": args.subdomain,
            "branding": {
                "primary_color": args.primary_color,
                "company_name": args.name
            },
            "features": {
                "receipt_scanning": True,
                "reports": True,
                "api_access": args.tier == "enterprise",
                "max_users": {"basic": 5, "professional": 20, "enterprise": 100}.get(args.tier, 5),
                "max_jobs": {"basic": 50, "professional": 200, "enterprise": 1000}.get(args.tier, 50)
            },
            "subscription_tier": args.tier,
            "subscription_status": "active"
        }
        
        tenant_response = supabase.table("tenants").insert(tenant_data).execute()
        if not tenant_response.data:
            print("Error: Failed to create tenant")
            sys.exit(1)
        
        tenant_id = tenant_response.data[0]["id"]
        print(f"✓ Tenant created: {tenant_id}")
        
        # 3. Create admin user in Supabase Auth
        print("Creating admin user...")
        auth_response = supabase.auth.admin.create_user({
            "email": args.admin_email,
            "password": admin_password,
            "email_confirm": True
        })
        
        if not auth_response.user:
            print("Error: Failed to create auth user")
            # Rollback tenant
            supabase.table("tenants").delete().eq("id", tenant_id).execute()
            sys.exit(1)
        
        user_id = auth_response.user.id
        print(f"✓ Auth user created: {user_id}")
        
        # 4. Create user profile
        print("Creating user profile...")
        user_data = {
            "id": user_id,
            "tenant_id": tenant_id,
            "email": args.admin_email,
            "name": args.admin_name or "Admin",
            "role": "admin",
            "is_active": True
        }
        
        supabase.table("users").insert(user_data).execute()
        print("✓ User profile created")
        
        # Success!
        print("\n" + "=" * 50)
        print("✅ TENANT ONBOARDED SUCCESSFULLY!")
        print("=" * 50)
        print(f"\nCompany: {args.name}")
        print(f"Organization Code: {args.subdomain}")
        print(f"Admin Email: {args.admin_email}")
        print(f"Subscription: {args.tier.title()}")
        print(f"\nTenant ID: {tenant_id}")
        print(f"User ID: {user_id}")
        print("\nThe admin can now sign in at your application URL.")
        print("New users can sign up using the organization code.")
        
    except Exception as e:
        print(f"\nError during onboarding: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
