<<<<<<< HEAD
# Elite Wall Pro - Production Job Costing System

A production-grade, multi-tenant job costing application built with **FastAPI**, **Streamlit**, and **Supabase**.
=======
# Elite Wall Pro - Production SaaS Platform

Enterprise-grade job costing software for construction companies.
>>>>>>> feature/migration-to-fastapi

## 🏗️ Architecture

```
<<<<<<< HEAD
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
=======
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Streamlit     │ ─────→  │   FastAPI        │ ─────→  │  Supabase   │
│   Frontend      │  HTTP   │   Backend        │  SQL    │  PostgreSQL │
│  (Railway)      │         │   (Railway)      │         │             │
└─────────────────┘         └──────────────────┘         └─────────────┘
```

### Technology Stack

**Backend:**
- FastAPI (async Python web framework)
- Supabase (PostgreSQL + Auth + Storage)
- Pydantic (data validation)
- JWT authentication

**Frontend:**
- Streamlit (Python UI framework)
- Plotly (interactive charts)
- httpx/requests (API client)

**Deployment:**
- Railway.app (Platform-as-a-Service)
- Automatic SSL/HTTPS
- Auto-scaling
- GitHub CI/CD

## 🚀 Quick Start - Railway Deployment

### Step 1: Prerequisites

1. **Railway Account:** Sign up at [railway.app](https://railway.app)
2. **Supabase Project:** Create at [supabase.com](https://supabase.com)
3. **GitHub Repository:** Fork or push this code

### Step 2: Deploy Backend

```bash
# In Railway Dashboard
1. New Project → "Deploy from GitHub"
2. Select repository
3. Select "backend" folder as root directory
4. Add environment variables (see backend/README.md)
5. Deploy
```

**Required Environment Variables:**
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
API_SECRET_KEY=your-secure-key
CORS_ORIGINS=["https://your-frontend.up.railway.app"]
```

### Step 3: Deploy Frontend

```bash
# In Railway Dashboard (same project)
1. Add New Service → "GitHub Repo"
2. Select "frontend" folder as root directory
3. Add environment variables
4. Deploy
```

**Required Environment Variables:**
```
API_URL=https://your-backend.up.railway.app
```

### Step 4: Configure CORS

After frontend deploys:
1. Copy frontend URL
2. Update backend `CORS_ORIGINS` environment variable
3. Restart backend service

### Step 5: Initialize Database

Run Supabase SQL Editor:
```sql
-- See docs/database_schema.sql for full schema
-- Or use Supabase migration tools
```

### Step 6: Access Your App

Frontend URL: `https://your-frontend-name.up.railway.app`
>>>>>>> feature/migration-to-fastapi

## 📁 Project Structure

```
elite-wall-pro/
<<<<<<< HEAD
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
=======
│
├── backend/                 # FastAPI Backend
│   ├── main.py             # App entry point
│   ├── config.py           # Settings
│   ├── database.py         # Supabase client
│   ├── auth.py             # JWT authentication
│   ├── routers/            # API endpoints
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   ├── costs.py
│   │   └── ...
│   ├── requirements.txt
│   ├── railway.toml
│   └── README.md
│
├── frontend/               # Streamlit Frontend
│   ├── app.py             # Main dashboard
│   ├── api_client.py      # Backend API client
│   ├── config.py          # Frontend settings
│   ├── pages/             # Multi-page app
│   │   ├── 1_Dashboard.py
│   │   ├── 2_Jobs.py
│   │   ├── 3_Cost_Entry.py
│   │   └── ...
│   ├── components/        # Reusable UI components
│   │   ├── auth.py
│   │   ├── sidebar.py
│   │   └── shared_styles.py
│   ├── requirements.txt
│   ├── railway.toml
│   └── README.md
│
├── .env.example           # Environment template
├── README.md              # This file
└── START.md               # Deployment guide
```

## 🔐 Security Features

- Row-Level Security (RLS) in Supabase
- JWT-based authentication
- HTTPS-only (enforced by Railway)
- CORS protection
- Environment-based secrets
- No hardcoded credentials

## 💰 Pricing Estimate

**Railway (per month):**
- Backend: ~$5 (500 MB RAM, shared CPU)
- Frontend: ~$5 (500 MB RAM, shared CPU)
- Total: ~$10/month

**Supabase:**
- Free tier: 500 MB database, 1 GB storage
- Paid: $25/month for production

**Total Cost:** ~$10-35/month (scales with usage)

## 🔄 Development Workflow

### Local Development

```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
pip install -r requirements.txt
export API_URL=http://localhost:8000
streamlit run app.py
```

### Git Workflow

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main

# Railway auto-deploys on push
```

### Environment Management

- Development: `.env` files locally
- Production: Railway environment variables UI
- Never commit `.env` files

## 📊 Features

### Financial Management
- Revenue & profit tracking
- Budget vs actual analysis
- Change order management
- Risk alerts for over-budget jobs

### Job Costing
- Multi-job tracking
- Category-based cost breakdown
- Weekly cost entries
- Real-time margin calculations

### Reporting
- Financial dashboards
- Job profitability reports
- Custom date ranges
- Export capabilities

### Multi-Tenancy
- Isolated tenant data
- Custom branding per tenant
- Role-based access control

## 🛠 Customization

### Branding
Edit in Supabase `tenants.branding`:
```json
{
  "primary_color": "#4A7C59",
  "company_name": "Your Company",
  "logo_url": "https://..."
}
```

### Features
Toggle in Supabase `tenants.features`:
```json
{
  "receipt_scanning": true,
  "reports": true,
  "api_access": false,
  "max_users": 10
}
```

## 📈 Scaling

### Performance Optimization
- Railway auto-scales based on traffic
- Supabase connection pooling
- FastAPI async operations
- Streamlit caching

### Database Optimization
- Indexed foreign keys
- Efficient queries
- RLS policies for security
- Regular vacuum and analyze

## 🚨 Troubleshooting

### Backend Won't Start
```bash
railway logs --service backend
# Check for:
# - Missing environment variables
# - Database connection errors
# - Import errors
```

### Frontend Can't Connect
```bash
# Verify API_URL is correct
railway variables --service frontend

# Test backend health
curl https://your-backend.up.railway.app/health
```

### Database Errors
```bash
# Check Supabase connection
# Verify RLS policies allow access
# Check user has correct tenant_id
```

## 📚 Documentation

- **Backend API:** `https://your-backend.up.railway.app/docs`
- **Frontend:** `frontend/README.md`
- **Backend:** `backend/README.md`
- **Deployment:** `START.md`

## 🤝 Support

For deployment issues:
1. Check Railway logs
2. Verify environment variables
3. Test locally first
4. Check database connectivity

## 📝 License

Proprietary - Elite Wall Pro

## 🚀 Next Steps

After deployment:
1. Create first user account
2. Set up company branding
3. Import customer/vendor data
4. Start logging jobs and costs
5. Monitor financial metrics

**Welcome to Elite Wall Pro!** 🏗️
>>>>>>> feature/migration-to-fastapi
