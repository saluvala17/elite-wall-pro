# 🚀 Railway Deployment Guide - Elite Wall Pro

Complete step-by-step guide to deploy Elite Wall Pro on Railway.app.

## ⏱ Estimated Time: 15-20 minutes

---

## 📋 Prerequisites Checklist

- [ ] Railway account (sign up at railway.app)
- [ ] Supabase account (sign up at supabase.com)
- [ ] GitHub account
- [ ] Git installed locally
- [ ] This code pushed to GitHub repository

---

## 🗄️ Step 1: Setup Supabase Database (5 mins)

### 1.1 Create Supabase Project

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Click "New Project"
3. Fill in:
   - Name: `elite-wall-pro`
   - Database Password: (save this!)
   - Region: Choose closest to your users
4. Click "Create Project" (wait 2-3 minutes)

### 1.2 Get Supabase Credentials

1. In Supabase dashboard, go to **Settings** → **API**
2. Copy these values (you'll need them later):
   ```
   URL: https://xxxxx.supabase.co
   anon/public key: eyJxxx...
   service_role key: eyJxxx... (keep secret!)
   ```

### 1.3 Setup Database Schema

1. In Supabase, go to **SQL Editor**
2. Create a new query
3. Copy-paste the schema from `docs/database_schema.sql` (if available)
   Or run:
   ```sql
   -- Create tables, policies, etc.
   -- See your project docs for full schema
   ```
4. Click "Run"

### 1.4 Create First Tenant

```sql
INSERT INTO tenants (name, subdomain, branding) VALUES (
  'Demo Company',
  'demo',
  '{"primary_color": "#4A7C59", "company_name": "Demo Construction"}'
);
```

---

## 🚂 Step 2: Deploy Backend to Railway (7 mins)

### 2.1 Create Railway Project

1. Go to [railway.app/dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select your `elite-wall-pro` repository

### 2.2 Configure Backend Service

1. Railway will detect your code
2. Click **Settings**:
   - **Root Directory:** `backend`
   - **Service Name:** `backend`
3. Click **Deploy**

### 2.3 Set Backend Environment Variables

Click **Variables** tab and add:

```bash
# Supabase (from Step 1.2)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...

# API Security
API_SECRET_KEY=your-random-secure-key-change-this-to-something-long-and-random

# Debug (set to false for production)
API_DEBUG=false

# CORS (will update after frontend deploys)
CORS_ORIGINS=["http://localhost:8501"]

# Optional: AI Features
ANTHROPIC_API_KEY=sk-ant-xxx
```

**Generate secure API_SECRET_KEY:**
```bash
# Run locally:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.4 Get Backend URL

1. Go to **Settings** → **Networking**
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://backend-production-xxxx.up.railway.app`)
4. **Save this URL** - you'll need it for frontend

### 2.5 Verify Backend Works

```bash
# Test health endpoint
curl https://your-backend-url.up.railway.app/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"2.0.0"}
```

---

## 🎨 Step 3: Deploy Frontend to Railway (5 mins)

### 3.1 Add Frontend Service

1. In same Railway project, click **+ New**
2. Select **GitHub Repo** (same repo)
3. Click **Settings**:
   - **Root Directory:** `frontend`
   - **Service Name:** `frontend`
4. Click **Deploy**

### 3.2 Set Frontend Environment Variables

Click **Variables** tab and add:

```bash
# Backend API URL (from Step 2.4)
API_URL=https://your-backend-url.up.railway.app

# Streamlit Config (optional)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_THEME_PRIMARY_COLOR=#4A7C59
```

### 3.3 Get Frontend URL

1. Go to **Settings** → **Networking**
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://frontend-production-xxxx.up.railway.app`)
4. **This is your app URL!** 🎉

---

## 🔒 Step 4: Update CORS (2 mins)

### 4.1 Update Backend CORS

1. Go back to **backend** service
2. Click **Variables**
3. Update `CORS_ORIGINS`:
   ```json
   ["https://your-frontend-url.up.railway.app","http://localhost:8501"]
   ```
4. Backend will auto-restart

---

## ✅ Step 5: Test Your Deployment (3 mins)

### 5.1 Test Backend

```bash
# Health check
curl https://your-backend.up.railway.app/health

# API docs (in browser)
https://your-backend.up.railway.app/docs
```

### 5.2 Test Frontend

1. Open: `https://your-frontend.up.railway.app`
2. You should see login page
3. Sign up with new account
4. Explore the dashboard!

---

## 🐛 Troubleshooting

### Backend not starting?

```bash
# Check logs in Railway dashboard
# Look for:
# - Missing environment variables
# - Database connection errors
# - Import errors

# Common fixes:
# 1. Verify all environment variables are set
# 2. Check SUPABASE_URL doesn't have trailing slash
# 3. Ensure requirements.txt has all dependencies
```

### Frontend can't connect to backend?

```bash
# Check:
# 1. API_URL is correct (no trailing slash)
# 2. Backend is running (check health endpoint)
# 3. CORS_ORIGINS includes frontend URL
# 4. Both services are in same Railway project
```

### Database errors?

```bash
# Check Supabase:
# 1. Project is active
# 2. Schema is set up correctly
# 3. RLS policies allow access
# 4. Credentials are correct
```

### Can't sign up?

```bash
# Check:
# 1. Supabase auth is enabled
# 2. Tenant exists in database
# 3. Backend logs for errors
```

---

## 🎯 Post-Deployment Checklist

- [ ] Backend health check returns 200 OK
- [ ] Frontend loads without errors
- [ ] Can create account
- [ ] Can log in
- [ ] Dashboard loads with data
- [ ] Can create a job
- [ ] Can log a cost

---

## 📊 Monitoring

### Railway Dashboard

1. **Metrics:** CPU, Memory, Network usage
2. **Logs:** Real-time application logs
3. **Deployments:** History and rollback
4. **Usage:** Billing and resource consumption

### Check Logs

```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs --service backend
railway logs --service frontend
```

---

## 🔄 Making Updates

### Deploy Changes

```bash
# Make your code changes
git add .
git commit -m "Description of changes"
git push origin main

# Railway auto-deploys!
# Watch deployment in dashboard
```

### Rollback

1. Go to **Deployments** tab
2. Find previous working deployment
3. Click "Redeploy"

---

## 💡 Pro Tips

1. **Environment Variables:** Keep production secrets in Railway, never in code
2. **Logging:** Check Railway logs regularly
3. **Monitoring:** Set up uptime monitoring (UptimeRobot, etc.)
4. **Backups:** Supabase does daily backups automatically
5. **Scaling:** Railway auto-scales, but monitor usage
6. **Custom Domain:** Add your own domain in Railway settings

---

## 📚 Next Steps

1. **Customize Branding:** Update tenant branding in Supabase
2. **Add Users:** Create team accounts
3. **Import Data:** Load customers, vendors
4. **Configure Features:** Enable/disable features per tenant
5. **Train Team:** Share user guides

---

## 🆘 Getting Help

1. **Railway Docs:** [docs.railway.app](https://docs.railway.app)
2. **Supabase Docs:** [supabase.com/docs](https://supabase.com/docs)
3. **Railway Discord:** Community support
4. **Logs:** Always check logs first

---

## 🎉 Success!

Your Elite Wall Pro SaaS platform is now live on Railway!

**URLs:**
- Frontend: `https://your-frontend.up.railway.app`
- Backend API: `https://your-backend.up.railway.app/docs`
- Supabase: `https://app.supabase.com/project/xxx`

**Estimated Monthly Cost:**
- Railway: ~$10 (2 services)
- Supabase: Free tier or $25
- **Total: ~$10-35/month**

---

## 📝 Deployment Summary

```
✅ Supabase database created
✅ Backend deployed to Railway
✅ Frontend deployed to Railway
✅ CORS configured
✅ Environment variables set
✅ SSL/HTTPS enabled (automatic)
✅ Auto-scaling enabled (automatic)
✅ Monitoring available
✅ Ready for production!
```

**Welcome to production! 🚀**
