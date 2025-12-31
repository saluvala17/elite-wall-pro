# Elite Wall Pro - Production Job Costing System

A production-grade, multi-tenant job costing application built with **FastAPI**, **Streamlit**, and **Supabase**.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ELITE WALL PRO                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────────┐   │
│  │  Streamlit  │────▶│   FastAPI   │────▶│        Supabase             │   │
│  │  Frontend   │     │   Backend   │     │  ┌─────────┐ ┌───────────┐  │   │
│  │             │     │             │     │  │PostgreSQL│ │   Auth    │  │   │
│  │  - UI/UX    │     │  - REST API │     │  │ Database │ │  Service  │  │   │
│  │  - Charts   │     │  - Auth     │     │  └─────────┘ └───────────┘  │   │
│  │  - Forms    │     │  - Business │     │  ┌─────────┐ ┌───────────┐  │   │
│  │             │     │    Logic    │     │  │ Storage │ │ Realtime  │  │   │
│  └─────────────┘     └─────────────┘     │  │ (Files) │ │  Updates  │  │   │
│                                          │  └─────────┘ └───────────┘  │   │
│                                          └─────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Multi-Tenant Architecture
- **Tenant Isolation**: Complete data isolation per customer
- **Custom Branding**: Logo, colors, terminology per tenant
- **Feature Flags**: Enable/disable features per tenant
- **Usage Tracking**: Monitor API calls and storage per tenant

### Core Functionality
- **Job Management**: Create, track, and manage construction jobs
- **Cost Tracking**: Weekly cost entry with budget vs actual
- **Receipt Scanning**: AI-powered receipt parsing with Claude
- **Customer/Vendor Management**: CRM-lite functionality
- **Employee Management**: Track team members and assignments
- **Reports & Analytics**: Profitability, budget tracking, trends

### Production Features
- **JWT Authentication**: Secure token-based auth via Supabase
- **Role-Based Access Control**: Admin, Manager, Employee roles
- **API Rate Limiting**: Protect against abuse
- **Audit Logging**: Track all data changes
- **Automated Backups**: Supabase handles backups
- **Row-Level Security**: PostgreSQL RLS policies

## 📁 Project Structure

```
elite-wall-pro/
├── api/                      # FastAPI Backend
│   ├── main.py              # App entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Supabase connection
│   ├── auth.py              # Authentication helpers
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── job.py
│   │   ├── cost.py
│   │   └── customer.py
│   ├── routers/             # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tenants.py
│   │   ├── jobs.py
│   │   ├── costs.py
│   │   ├── customers.py
│   │   ├── vendors.py
│   │   ├── employees.py
│   │   └── receipts.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── tenant_service.py
│   │   ├── job_service.py
│   │   ├── cost_service.py
│   │   └── receipt_service.py
│   └── requirements.txt
│
├── frontend/                 # Streamlit Frontend
│   ├── app.py               # Main Streamlit app
│   ├── config.py            # Frontend config
│   ├── api_client.py        # FastAPI client
│   ├── components/          # Reusable UI components
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── sidebar.py
│   │   ├── charts.py
│   │   └── forms.py
│   ├── pages/               # Streamlit pages
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Jobs.py
│   │   ├── 3_Cost_Entry.py
│   │   ├── 4_Customers.py
│   │   ├── 5_Vendors.py
│   │   ├── 6_Reports.py
│   │   ├── 7_Employees.py
│   │   └── 8_Settings.py
│   ├── .streamlit/
│   │   └── config.toml
│   └── requirements.txt
│
├── shared/                   # Shared utilities
│   ├── __init__.py
│   ├── constants.py
│   └── utils.py
│
├── scripts/                  # Setup & deployment scripts
│   ├── setup_supabase.sql   # Database schema
│   ├── seed_data.sql        # Sample data
│   └── onboard_tenant.py    # New customer onboarding
│
├── docs/                     # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── ONBOARDING.md
│
├── docker-compose.yml        # Local development
├── .env.example             # Environment template
└── README.md
```

## 🛠️ Quick Start

### 1. Prerequisites
- Python 3.11+
- Supabase account (free tier works)
- Anthropic API key (for receipt scanning)

### 2. Setup Supabase

1. Create a new Supabase project at https://supabase.com
2. Run the schema script: `scripts/setup_supabase.sql`
3. Copy your project URL and anon key

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Install Dependencies

```bash
# Backend
cd api && pip install -r requirements.txt

# Frontend
cd frontend && pip install -r requirements.txt
```

### 5. Run the Application

```bash
# Terminal 1: Start API
cd api && uvicorn main:app --reload --port 8000

# Terminal 2: Start Frontend
cd frontend && streamlit run app.py --server.port 8501
```

### 6. Access the Application
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## 🆕 Onboarding New Customers

### Option 1: Script (Recommended)
```bash
python scripts/onboard_tenant.py \
  --name "Acme Construction" \
  --subdomain "acme" \
  --admin-email "admin@acme.com" \
  --primary-color "#2E7D32"
```

### Option 2: API
```bash
curl -X POST http://localhost:8000/api/v1/tenants \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Construction",
    "subdomain": "acme",
    "settings": {
      "primary_color": "#2E7D32",
      "logo_url": "https://..."
    }
  }'
```

### Option 3: Admin Dashboard
Navigate to Settings → Tenant Management → Add New Tenant

## 🔐 Security

- **Authentication**: Supabase Auth with JWT tokens
- **Authorization**: Row-Level Security (RLS) policies
- **Data Isolation**: Tenant ID on every table
- **API Security**: Rate limiting, CORS, input validation
- **Secrets**: Environment variables, never in code

## 📊 Database Schema

See `scripts/setup_supabase.sql` for complete schema.

Key tables:
- `tenants` - Customer organizations
- `users` - User accounts (linked to Supabase Auth)
- `jobs` - Construction jobs
- `weekly_costs` - Cost entries
- `cost_line_items` - Detailed receipt line items
- `customers` - GCs and clients
- `vendors` - Suppliers
- `employees` - Team members

## 🚀 Deployment

### Recommended: Railway + Supabase
1. Deploy API to Railway
2. Deploy Frontend to Streamlit Cloud
3. Use Supabase hosted database

See `docs/DEPLOYMENT.md` for detailed instructions.

## 📄 License

Proprietary - Forge N Systems

## 🤝 Support

Contact: support@forge-n-systems.com
