# Elite Wall Pro - Backend API

Production-grade FastAPI backend for construction job costing.

## 🚀 Railway Deployment

### Prerequisites
- Railway account
- Supabase database

### Environment Variables (Required)

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key  # Optional

# API Configuration
API_SECRET_KEY=your-secure-secret-key-change-me
API_DEBUG=false

# CORS (Add your frontend Railway URL)
CORS_ORIGINS=["https://your-frontend.up.railway.app","http://localhost:8501"]

# Optional: AI Features
ANTHROPIC_API_KEY=sk-ant-xxx  # For AI-powered features
```

### Deploy to Railway

1. **Create New Service:**
   ```bash
   # From Railway dashboard
   New Project → Deploy from GitHub → Select backend folder
   ```

2. **Set Environment Variables:**
   - Go to Variables tab
   - Add all required environment variables listed above

3. **Deployment:**
   - Railway will automatically detect `railway.toml`
   - Build and deploy using Nixpacks
   - Health check at `/health`

### API Endpoints

- **Health:** `GET /health`
- **Docs:** `GET /docs`
- **Auth:** `POST /api/v1/auth/signin`, `POST /api/v1/auth/signup`
- **Jobs:** `GET /api/v1/jobs`, `POST /api/v1/jobs`, etc.
- **Costs:** `GET /api/v1/costs`, `POST /api/v1/costs`, etc.

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run server
uvicorn main:app --reload --port 8000
```

### Architecture

```
backend/
├── main.py              # FastAPI app entry point
├── config.py            # Settings management
├── database.py          # Supabase client
├── auth.py              # Authentication utilities
├── routers/             # API route modules
│   ├── auth.py
│   ├── jobs.py
│   ├── costs.py
│   └── ...
└── railway.toml         # Railway config
```

### Security Features

- JWT authentication with Supabase
- CORS protection
- Row-level security (RLS) via Supabase
- Global exception handling
- Request logging

### Performance

- Async FastAPI for high throughput
- Connection pooling with Supabase
- Health check endpoint for load balancers
- Automatic restarts on failure

## 📚 API Documentation

Once deployed, visit:
- Swagger UI: `https://your-backend.up.railway.app/docs`
- ReDoc: `https://your-backend.up.railway.app/redoc`

## 🔒 Authentication Flow

1. User signs in via `/api/v1/auth/signin`
2. Backend validates credentials with Supabase
3. Returns JWT access token
4. Frontend includes token in Authorization header
5. Protected routes verify token before processing

## 🛠 Troubleshooting

### Build Fails
- Check `requirements.txt` for conflicting versions
- Verify Python version compatibility (3.11+)

### Database Connection Issues
- Verify SUPABASE_URL and keys are correct
- Check Supabase project is active
- Ensure RLS policies allow access

### CORS Errors
- Add frontend URL to CORS_ORIGINS
- Include protocol (https://)
- Restart backend after env var changes

## 📧 Support

For issues, check Railway logs:
```bash
railway logs --service backend
```
