# backend/app/db/rls_policies.sql (Run via init_db.py)
"""
RLS Policies: Enforce tenant isolation.
Enable RLS on tables, set session var in middleware.
Best practices: , , , , 
"""
-- Enable RLS on key tables
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE bills ENABLE ROW LEVEL SECURITY;  -- POS
ALTER TABLE inventory_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE audits ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their tenant's rows
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Similar for other tables...
CREATE POLICY tenant_isolation ON bills
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Super users bypass (role check in app)
CREATE POLICY super_user_bypass ON users FOR ALL
    USING (EXISTS (SELECT 1 FROM users u WHERE u.id = auth.uid() AND u.role = 'super_user'));