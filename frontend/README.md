# Elite Wall Pro - Frontend

Professional Streamlit dashboard for construction job costing.

## 🚀 Railway Deployment

### Prerequisites
- Backend API deployed and running
- Railway account

### Environment Variables (Required)

```bash
# Backend API URL (Your Railway backend URL)
API_URL=https://your-backend.up.railway.app

# Streamlit Configuration (Optional)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_THEME_PRIMARY_COLOR=#4A7C59
```

### Deploy to Railway

1. **Create New Service:**
   ```bash
   # From Railway dashboard
   New Project → Deploy from GitHub → Select frontend folder
   ```

2. **Set Environment Variables:**
   - Go to Variables tab
   - Set `API_URL` to your backend Railway URL

3. **Deployment:**
   - Railway will automatically detect `railway.toml`
   - Build and deploy using Nixpacks
   - Streamlit will run on assigned port

### Access Your Dashboard

After deployment, Railway provides a public URL:
```
https://your-frontend.up.railway.app
```

## 📱 Features

### Pages
- **Dashboard:** Financial KPIs, job cards, alerts
- **Jobs:** Job management and tracking
- **Cost Entry:** Log costs and invoices
- **Customers:** Customer database
- **Vendors:** Vendor management
- **Reports:** Financial reports
- **Employees:** Employee tracking
- **Settings:** Account and preferences

### Authentication
- Secure JWT-based authentication
- Session management
- Auto-refresh on token expiry

### Dashboard Highlights
- Real-time financial metrics
- Job progress tracking
- Risk alerts
- Budget vs actual analysis
- Interactive charts

## 🛠 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_URL=http://localhost:8000

# Run Streamlit
streamlit run app.py
```

Visit: `http://localhost:8501`

## 📁 Project Structure

```
frontend/
├── app.py                    # Main dashboard
├── config.py                 # Frontend settings
├── api_client.py             # FastAPI client
├── pages/                    # Multi-page app
│   ├── 1_Dashboard.py
│   ├── 2_Jobs.py
│   ├── 3_Cost_Entry.py
│   └── ...
├── components/               # Reusable components
│   ├── auth.py              # Auth UI
│   ├── sidebar.py           # Navigation
│   └── shared_styles.py     # CSS
├── .streamlit/
│   └── config.toml          # Streamlit config
├── requirements.txt
└── railway.toml
```

## 🎨 Customization

### Branding
Edit tenant branding via Settings page:
- Primary color
- Company name
- Logo upload

### Theme
Modify `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#4A7C59"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## 🔒 Security

- No direct database access (all via backend API)
- JWT tokens stored in session state
- Automatic token refresh
- Secure HTTPS on Railway

## 🚨 Troubleshooting

### Cannot Connect to Backend
- Verify `API_URL` environment variable
- Ensure backend is running
- Check backend CORS allows frontend domain

### Blank Page / Loading Forever
- Check Railway logs: `railway logs --service frontend`
- Verify port binding: Streamlit uses `$PORT` from Railway
- Check `railway.toml` start command

### Session Expired Errors
- Backend JWT token may have expired
- Log in again
- Check backend `ACCESS_TOKEN_EXPIRE_MINUTES`

### Styling Issues
- Clear browser cache
- Check if `shared_styles.py` loaded
- Verify CSS in browser DevTools

## 📊 Dashboard Metrics

### Financial Health
- Total Revenue & Margin
- Cash Flow (Change Orders)
- Active Jobs Count
- Risk Alerts

### Job Cards
- Dual progress bars (Budget vs Actual)
- Financial variance
- Profit margins
- Last cost entry date

### Analytics
- Budget vs Actual charts
- Category breakdown
- Top 5 jobs benchmark

## 🔄 Updates

Railway auto-deploys on git push:
```bash
git push origin main
```

Monitor deployment:
```bash
railway status --service frontend
```

## 📧 Support

Check logs for errors:
```bash
railway logs --service frontend
```

For API issues, check backend logs.
