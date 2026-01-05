# Elite Wall Pro - Production SaaS Platform

Enterprise-grade job costing software for construction companies.

## 🏗️ Architecture

```
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

## 📁 Project Structure

```
elite-wall-pro/
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
