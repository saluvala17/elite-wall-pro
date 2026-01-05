# Elite Wall Pro - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS / CLIENTS                          │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTPS (SSL)
                 │
┌────────────────▼─────────────────────────────────────────────────┐
│                      RAILWAY PLATFORM                             │
│  ┌──────────────────────┐        ┌──────────────────────┐        │
│  │  Frontend Service    │        │  Backend Service     │        │
│  │                      │        │                      │        │
│  │  Streamlit App       │◄──────►│  FastAPI App         │        │
│  │  - UI/UX Layer       │  HTTP  │  - Business Logic    │        │
│  │  - Session State     │        │  - API Endpoints     │        │
│  │  - Charts/Viz        │        │  - Authentication    │        │
│  │                      │        │  - Data Processing   │        │
│  │  Port: $PORT         │        │  Port: $PORT         │        │
│  └──────────────────────┘        └──────┬───────────────┘        │
│                                          │                        │
└──────────────────────────────────────────┼────────────────────────┘
                                           │
                                           │ PostgreSQL Protocol
                                           │
                            ┌──────────────▼──────────────┐
                            │   SUPABASE PLATFORM         │
                            │  ┌────────────────────────┐ │
                            │  │  PostgreSQL Database   │ │
                            │  │  - Multi-tenant data   │ │
                            │  │  - Row-Level Security  │ │
                            │  │  - Automatic backups   │ │
                            │  └────────────────────────┘ │
                            │  ┌────────────────────────┐ │
                            │  │  Auth Service          │ │
                            │  │  - JWT tokens          │ │
                            │  │  - User management     │ │
                            │  └────────────────────────┘ │
                            │  ┌────────────────────────┐ │
                            │  │  Storage (optional)    │ │
                            │  │  - File uploads        │ │
                            │  └────────────────────────┘ │
                            └─────────────────────────────┘
```

## 🔄 Request Flow

### 1. User Authentication Flow
```
User → Frontend → Backend API → Supabase Auth → Backend → Frontend → User
                                      │
                                      └─ JWT Token Generated
```

**Steps:**
1. User enters credentials in Streamlit login form
2. Frontend sends POST to `/api/v1/auth/signin`
3. Backend validates with Supabase Auth
4. Backend generates JWT access token
5. Frontend stores token in session state
6. All subsequent requests include token in Authorization header

### 2. Data Fetch Flow
```
User Action → Frontend → Backend API → Supabase DB → Backend → Frontend → Render
                  │
                  └─ Includes JWT Token
```

**Steps:**
1. User navigates to page (e.g., Jobs page)
2. Frontend calls API: `GET /api/v1/jobs` with JWT
3. Backend validates JWT
4. Backend queries Supabase with RLS filtering by tenant_id
5. Backend returns JSON data
6. Frontend renders data in Streamlit components

### 3. Data Mutation Flow
```
User Input → Frontend → Backend API → Validation → Supabase DB → Response
                                           │
                                           └─ Pydantic Schemas
```

**Steps:**
1. User submits form (e.g., Create Job)
2. Frontend sends POST/PUT/DELETE with JSON payload
3. Backend validates data using Pydantic schemas
4. Backend executes database transaction
5. Backend returns success/error response
6. Frontend updates UI and shows notification

## 📦 Component Breakdown

### Frontend (Streamlit)

**Purpose:** User interface and experience layer

**Responsibilities:**
- Render UI components
- Handle user interactions
- Manage session state
- Display data visualizations
- Form validation (client-side)
- Call backend API

**Technology:**
- Streamlit (Python UI framework)
- Plotly (charts)
- Requests/HTTPX (API client)

**Files:**
```
frontend/
├── app.py                 # Main dashboard
├── pages/                 # Multi-page app
│   ├── 1_Dashboard.py
│   ├── 2_Jobs.py
│   └── ...
├── components/            # Reusable UI
│   ├── auth.py
│   ├── sidebar.py
│   └── shared_styles.py
├── api_client.py          # Backend communication
├── config.py              # Settings
└── .streamlit/config.toml # Streamlit config
```

### Backend (FastAPI)

**Purpose:** Business logic and data access layer

**Responsibilities:**
- API endpoints (RESTful)
- Authentication & authorization
- Data validation
- Business logic
- Database queries
- Error handling
- Logging

**Technology:**
- FastAPI (async web framework)
- Pydantic (data validation)
- Supabase client (database)
- Python-JOSE (JWT)

**Files:**
```
backend/
├── main.py                # FastAPI app
├── config.py              # Settings
├── database.py            # Supabase client
├── auth.py                # JWT utilities
└── routers/               # API modules
    ├── auth.py            # /api/v1/auth/*
    ├── jobs.py            # /api/v1/jobs/*
    ├── costs.py           # /api/v1/costs/*
    └── ...
```

### Database (Supabase/PostgreSQL)

**Purpose:** Data persistence and security

**Responsibilities:**
- Store all application data
- Enforce data integrity (constraints)
- Row-level security (multi-tenancy)
- User authentication
- Automatic backups

**Key Tables:**
- `tenants` - Multi-tenant isolation
- `users` - User accounts
- `jobs` - Construction jobs
- `weekly_costs` - Cost tracking
- `customers`, `vendors`, `employees`

**Security:**
- RLS policies filter by tenant_id
- Foreign key constraints
- Indexed columns for performance

## 🔐 Security Architecture

### Authentication

**Method:** JWT (JSON Web Tokens)

**Flow:**
1. User logs in → Supabase validates credentials
2. Backend generates JWT with user_id, tenant_id
3. Frontend stores JWT in session state (memory)
4. Every API request includes: `Authorization: Bearer <token>`
5. Backend validates JWT signature and expiry
6. Backend extracts tenant_id from JWT for RLS

**Token Structure:**
```json
{
  "user_id": "uuid",
  "tenant_id": "uuid",
  "role": "admin",
  "exp": 1234567890
}
```

### Authorization

**Multi-Tenancy:**
- Each user belongs to ONE tenant
- All queries filtered by tenant_id
- RLS enforced at database level
- No cross-tenant data access

**Role-Based Access:**
- `super_admin` - Platform admin
- `admin` - Tenant admin
- `manager` - Can manage jobs
- `employee` - Limited access
- `viewer` - Read-only

### Data Protection

**At Rest:**
- Supabase encrypts all data
- Passwords hashed with bcrypt
- Sensitive fields encrypted

**In Transit:**
- HTTPS enforced (Railway + Supabase)
- TLS 1.2+
- Secure websockets for Streamlit

**Application:**
- CORS restricted to known origins
- No SQL injection (parameterized queries)
- Input validation (Pydantic)
- Rate limiting (optional)

## 🚀 Deployment Architecture

### Railway Services

**Backend Service:**
```yaml
Name: backend
Type: Web Service
Port: $PORT (dynamic)
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Health Check: /health
Auto-scaling: Yes
```

**Frontend Service:**
```yaml
Name: frontend
Type: Web Service
Port: $PORT (dynamic)
Start Command: streamlit run app.py --server.port $PORT
Auto-scaling: Yes
```

### Environment Variables

**Backend:**
- `SUPABASE_URL` - Database connection
- `SUPABASE_ANON_KEY` - Public API key
- `SUPABASE_SERVICE_KEY` - Admin access
- `API_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed origins
- `API_DEBUG` - Debug mode

**Frontend:**
- `API_URL` - Backend API endpoint

### Networking

```
Internet → Railway Load Balancer → SSL Termination → Service
            ↓
         HTTPS
            ↓
    Custom Domain (optional)
```

**SSL/TLS:**
- Automatic SSL certificates
- HTTPS enforced
- HTTP → HTTPS redirect

**DNS:**
- Railway provides: `*.up.railway.app`
- Custom domains supported
- Automatic SSL for custom domains

## 📊 Data Flow Diagrams

### Job Creation Flow

```
┌─────────┐     1. Click "New Job"        ┌──────────┐
│ User    │─────────────────────────────→ │ Frontend │
└─────────┘                                └────┬─────┘
                                                │
                                         2. Show form
                                                │
┌─────────┐     3. Fill & Submit         ┌────▼─────┐
│ User    │─────────────────────────────→ │ Frontend │
└─────────┘                                └────┬─────┘
                                                │
                            4. POST /api/v1/jobs + JWT
                                                │
                                         ┌──────▼────┐
                                         │  Backend  │
                                         └──────┬────┘
                                                │
                                   5. Validate JWT & Data
                                                │
                                         ┌──────▼────────┐
                                         │  Supabase DB  │
                                         └──────┬────────┘
                                                │
                               6. INSERT job with tenant_id
                                                │
                                         ┌──────▼────┐
                                         │  Backend  │
                                         └──────┬────┘
                                                │
                                    7. Return job data
                                                │
                                         ┌──────▼─────┐
                                         │  Frontend  │
                                         └──────┬─────┘
                                                │
                                   8. Show success + redirect
                                                │
┌─────────┐                                ┌────▼─────┐
│ User    │←───────────────────────────────│ Frontend │
└─────────┘        9. See new job          └──────────┘
```

### Dashboard Load Flow

```
User → Frontend → API Call → Backend → Database → Backend → Frontend → Render
         │                                                        │
         └──────── Parallel API calls for different metrics ─────┘
              - GET /api/v1/jobs (active jobs)
              - GET /api/v1/costs/totals (cost summaries)
              - GET /api/v1/customers (for job cards)
```

## 🔧 Configuration Management

### Development
```
.env file (local) → Application reads → Uses local settings
```

### Production (Railway)
```
Railway Dashboard → Environment Variables → Injected at runtime
```

**Best Practices:**
- Never commit `.env` files
- Use `.env.example` as template
- Different values per environment
- Secrets in Railway variables only

## 📈 Scaling Strategy

### Horizontal Scaling
- Railway auto-scales based on traffic
- Multiple instances behind load balancer
- Stateless backend (scales easily)
- Streamlit scales per-session

### Database Scaling
- Supabase connection pooling
- Read replicas (Supabase Pro)
- Efficient indexes
- Query optimization

### Performance Optimization
- FastAPI async operations
- Streamlit caching (@st.cache_data)
- API response compression
- CDN for static assets (future)

## 🛠 Technology Choices

| Component | Technology | Why? |
|-----------|-----------|------|
| Frontend | Streamlit | Rapid Python UI development, built-in components |
| Backend | FastAPI | High performance, async, auto API docs |
| Database | PostgreSQL (Supabase) | Reliable, feature-rich, managed service |
| Deployment | Railway | Easy deployment, auto-scaling, affordable |
| Auth | Supabase Auth + JWT | Secure, scalable, OAuth support |
| Validation | Pydantic | Type safety, auto validation, IDE support |

## 📝 API Conventions

**Endpoints:**
```
/api/v1/{resource}        GET    - List all
/api/v1/{resource}        POST   - Create
/api/v1/{resource}/{id}   GET    - Get one
/api/v1/{resource}/{id}   PUT    - Update
/api/v1/{resource}/{id}   DELETE - Delete
```

**Response Format:**
```json
{
  "data": [...],
  "message": "Success",
  "status": 200
}
```

**Error Format:**
```json
{
  "detail": "Error message",
  "type": "ValueError",
  "status": 400
}
```

## 🔍 Monitoring & Observability

### Logging
- Structured logs (JSON)
- Timestamp, level, message
- Request/response logging
- Error stack traces

### Metrics (Railway Dashboard)
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

### Health Checks
- `/health` endpoint
- Database connectivity check
- Service status

---

This architecture provides a solid foundation for a scalable, secure SaaS application!
