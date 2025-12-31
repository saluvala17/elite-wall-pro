-- ============================================
-- ELITE WALL PRO - SUPABASE DATABASE SCHEMA
-- ============================================
-- Run this in your Supabase SQL Editor
-- This creates all tables with Row-Level Security

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TENANTS TABLE (Multi-tenant support)
-- ============================================
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB DEFAULT '{}'::jsonb,
    features JSONB DEFAULT '{
        "receipt_scanning": true,
        "reports": true,
        "api_access": false,
        "max_users": 10,
        "max_jobs": 100
    }'::jsonb,
    branding JSONB DEFAULT '{
        "primary_color": "#4A7C59",
        "secondary_color": "#8B4513",
        "logo_url": null,
        "company_name": null
    }'::jsonb,
    subscription_tier VARCHAR(50) DEFAULT 'basic',
    subscription_status VARCHAR(50) DEFAULT 'active',
    trial_ends_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- USERS TABLE (Extends Supabase Auth)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'employee' CHECK (role IN ('super_admin', 'admin', 'manager', 'employee', 'viewer')),
    phone VARCHAR(50),
    avatar_url TEXT,
    preferences JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- CUSTOMERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    notes TEXT,
    payment_terms VARCHAR(100),
    credit_limit DECIMAL(15,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- ============================================
-- VENDORS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS vendors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    vendor_type VARCHAR(100),
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    notes TEXT,
    payment_terms VARCHAR(100),
    tax_id VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- ============================================
-- EMPLOYEES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS employees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    employee_id VARCHAR(50),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    role VARCHAR(100),
    department VARCHAR(100),
    hourly_rate DECIMAL(10,2),
    hire_date DATE,
    termination_date DATE,
    emergency_contact VARCHAR(255),
    emergency_phone VARCHAR(50),
    address TEXT,
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- ============================================
-- JOBS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    job_number VARCHAR(50) NOT NULL,
    job_name VARCHAR(255) NOT NULL,
    customer_id UUID REFERENCES customers(id),
    
    -- Financial
    contract_amount DECIMAL(15,2) DEFAULT 0,
    pending_change_orders DECIMAL(15,2) DEFAULT 0,
    approved_change_orders DECIMAL(15,2) DEFAULT 0,
    
    -- Budget breakdown
    budget_insurance DECIMAL(15,2) DEFAULT 0,
    budget_labor DECIMAL(15,2) DEFAULT 0,
    budget_stamps DECIMAL(15,2) DEFAULT 0,
    budget_material DECIMAL(15,2) DEFAULT 0,
    budget_subs_bond DECIMAL(15,2) DEFAULT 0,
    budget_equipment DECIMAL(15,2) DEFAULT 0,
    budget_man_days INTEGER DEFAULT 0,
    
    -- Status & Dates
    status VARCHAR(50) DEFAULT 'estimate' CHECK (status IN ('estimate', 'active', 'on_hold', 'completed', 'cancelled')),
    start_date DATE,
    end_date DATE,
    estimated_completion DATE,
    
    -- Location
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    
    -- Metadata
    notes TEXT,
    tags TEXT[],
    is_archived BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    
    UNIQUE(tenant_id, job_number)
);

-- ============================================
-- WEEKLY COSTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS weekly_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    week_ending DATE NOT NULL,
    
    -- Cost actuals
    insurance_actual DECIMAL(15,2) DEFAULT 0,
    labor_actual DECIMAL(15,2) DEFAULT 0,
    stamps_actual DECIMAL(15,2) DEFAULT 0,
    material_actual DECIMAL(15,2) DEFAULT 0,
    subs_bond_actual DECIMAL(15,2) DEFAULT 0,
    equipment_actual DECIMAL(15,2) DEFAULT 0,
    man_days_actual INTEGER DEFAULT 0,
    
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    
    UNIQUE(tenant_id, job_id, week_ending)
);

-- ============================================
-- COST LINE ITEMS TABLE (Receipt details)
-- ============================================
CREATE TABLE IF NOT EXISTS cost_line_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    weekly_cost_id UUID REFERENCES weekly_costs(id),
    
    date DATE,
    vendor_name VARCHAR(255),
    description TEXT,
    category VARCHAR(50) CHECK (category IN ('insurance', 'labor', 'stamps', 'material', 'subs_bond', 'equipment', 'other')),
    amount DECIMAL(15,2) NOT NULL,
    
    receipt_number VARCHAR(100),
    receipt_image_url TEXT,
    
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- ============================================
-- AUDIT LOG TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID,
    old_data JSONB,
    new_data JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- SETTINGS TABLE (Per-tenant settings)
-- ============================================
CREATE TABLE IF NOT EXISTS settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    updated_by UUID REFERENCES users(id),
    
    UNIQUE(tenant_id, key)
);

-- ============================================
-- API KEYS TABLE (For API access)
-- ============================================
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    permissions JSONB DEFAULT '[]'::jsonb,
    rate_limit INTEGER DEFAULT 1000,
    expires_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX IF NOT EXISTS idx_users_tenant ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_customers_tenant ON customers(tenant_id);
CREATE INDEX IF NOT EXISTS idx_vendors_tenant ON vendors(tenant_id);
CREATE INDEX IF NOT EXISTS idx_employees_tenant ON employees(tenant_id);
CREATE INDEX IF NOT EXISTS idx_jobs_tenant ON jobs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(tenant_id, status);
CREATE INDEX IF NOT EXISTS idx_jobs_customer ON jobs(customer_id);
CREATE INDEX IF NOT EXISTS idx_weekly_costs_job ON weekly_costs(job_id);
CREATE INDEX IF NOT EXISTS idx_weekly_costs_week ON weekly_costs(tenant_id, week_ending);
CREATE INDEX IF NOT EXISTS idx_cost_line_items_job ON cost_line_items(job_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_tenant ON audit_logs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON audit_logs(created_at);

-- ============================================
-- ROW LEVEL SECURITY POLICIES
-- ============================================

-- Enable RLS on all tables
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_costs ENABLE ROW LEVEL SECURITY;
ALTER TABLE cost_line_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Helper function to get current user's tenant
CREATE OR REPLACE FUNCTION get_user_tenant_id()
RETURNS UUID AS $$
BEGIN
    RETURN (
        SELECT tenant_id FROM users WHERE id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Users can only see users in their tenant
CREATE POLICY users_tenant_isolation ON users
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Customers policy
CREATE POLICY customers_tenant_isolation ON customers
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Vendors policy
CREATE POLICY vendors_tenant_isolation ON vendors
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Employees policy
CREATE POLICY employees_tenant_isolation ON employees
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Jobs policy
CREATE POLICY jobs_tenant_isolation ON jobs
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Weekly costs policy
CREATE POLICY weekly_costs_tenant_isolation ON weekly_costs
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Cost line items policy
CREATE POLICY cost_line_items_tenant_isolation ON cost_line_items
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Audit logs policy
CREATE POLICY audit_logs_tenant_isolation ON audit_logs
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Settings policy
CREATE POLICY settings_tenant_isolation ON settings
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- API keys policy
CREATE POLICY api_keys_tenant_isolation ON api_keys
    FOR ALL USING (tenant_id = get_user_tenant_id());

-- Tenants: users can only see their own tenant
CREATE POLICY tenants_user_access ON tenants
    FOR SELECT USING (id = get_user_tenant_id());

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_vendors_updated_at BEFORE UPDATE ON vendors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_weekly_costs_updated_at BEFORE UPDATE ON weekly_costs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Function to calculate job totals
CREATE OR REPLACE FUNCTION get_job_cost_totals(p_job_id UUID)
RETURNS TABLE (
    insurance DECIMAL,
    labor DECIMAL,
    stamps DECIMAL,
    material DECIMAL,
    subs_bond DECIMAL,
    equipment DECIMAL,
    man_days INTEGER,
    total DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(wc.insurance_actual), 0) as insurance,
        COALESCE(SUM(wc.labor_actual), 0) as labor,
        COALESCE(SUM(wc.stamps_actual), 0) as stamps,
        COALESCE(SUM(wc.material_actual), 0) as material,
        COALESCE(SUM(wc.subs_bond_actual), 0) as subs_bond,
        COALESCE(SUM(wc.equipment_actual), 0) as equipment,
        COALESCE(SUM(wc.man_days_actual), 0)::INTEGER as man_days,
        COALESCE(SUM(wc.insurance_actual + wc.labor_actual + wc.stamps_actual + 
                     wc.material_actual + wc.subs_bond_actual + wc.equipment_actual), 0) as total
    FROM weekly_costs wc
    WHERE wc.job_id = p_job_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- SEED DATA FOR DEMO
-- ============================================

-- Insert a demo tenant (run this separately after creating first user)
-- INSERT INTO tenants (name, subdomain, branding) VALUES 
-- ('Demo Company', 'demo', '{"primary_color": "#4A7C59", "company_name": "Demo Construction"}');
