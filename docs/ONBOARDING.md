# Customer Onboarding Guide

## Overview

This guide explains how to onboard new customers (tenants) to Elite Wall Pro.

## Prerequisites

- Supabase project with schema deployed (`scripts/setup_supabase.sql`)
- Service role key configured
- Python 3.11+ with dependencies installed

## Onboarding Methods

### Method 1: Command-Line Script (Recommended)

The fastest way to onboard a new customer:

```bash
cd scripts

python onboard_tenant.py \
  --name "Acme Construction" \
  --subdomain "acme" \
  --admin-email "admin@acme.com" \
  --admin-name "John Smith" \
  --primary-color "#2E7D32" \
  --tier professional
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--name` | Yes | - | Company display name |
| `--subdomain` | Yes | - | Unique organization code (used for signup) |
| `--admin-email` | Yes | - | Initial admin user email |
| `--admin-name` | No | "Admin" | Admin user display name |
| `--primary-color` | No | #4A7C59 | Brand primary color |
| `--tier` | No | basic | Subscription tier (basic/professional/enterprise) |

The script will prompt for the admin password.

### Method 2: Super Admin Dashboard

If you have a super_admin account:

1. Log in to the application
2. Navigate to Settings → Tenant Management
3. Click "Add New Tenant"
4. Fill in the tenant details
5. Submit the form

### Method 3: Direct API Call

```bash
# Get super admin token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"superadmin@example.com","password":"..."}' \
  | jq -r '.access_token')

# Create tenant
curl -X POST http://localhost:8000/api/v1/tenants \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Construction",
    "subdomain": "acme",
    "branding": {
      "primary_color": "#2E7D32",
      "company_name": "Acme Construction"
    },
    "subscription_tier": "professional"
  }'
```

## Post-Onboarding Steps

### 1. Share Credentials

Send the following to the customer:

- **Application URL:** https://your-app.streamlit.app
- **Organization Code:** `{subdomain}`
- **Admin Email:** `{admin_email}`
- **Temporary Password:** (the one you set during onboarding)

### 2. Customer First Login

The admin should:
1. Go to the application URL
2. Sign in with email and temporary password
3. Change password (if required)
4. Configure company branding in Settings

### 3. Invite Additional Users

The admin can invite users by:
1. Sharing the Organization Code
2. Users sign up at the login page using "Create Account"
3. Admin can manage user roles in Settings → Users

## Subscription Tiers

| Feature | Basic | Professional | Enterprise |
|---------|-------|--------------|------------|
| Max Users | 5 | 20 | 100 |
| Max Jobs | 50 | 200 | 1000 |
| Receipt Scanning | ✅ | ✅ | ✅ |
| Reports | ✅ | ✅ | ✅ |
| API Access | ❌ | ❌ | ✅ |
| Price | $99/mo | $249/mo | $499/mo |

## Customization Options

### Branding

Each tenant can customize:
- Company name
- Primary color (affects buttons, accents)
- Secondary color
- Logo URL

### Features

Enable/disable per tenant:
- Receipt scanning
- Reports module
- API access
- User limits
- Job limits

## Troubleshooting

### "Subdomain already exists"
Choose a different organization code.

### "Failed to create auth user"
- Check if email already exists in Supabase Auth
- Verify SUPABASE_SERVICE_KEY is correct

### User can't sign up
- Verify they're using the correct Organization Code
- Check tenant is_active status
- Ensure user limit hasn't been reached

## Data Isolation

Each tenant's data is completely isolated through:
1. Row-Level Security (RLS) policies
2. tenant_id on every table
3. JWT token validation

Tenants cannot access other tenants' data.
