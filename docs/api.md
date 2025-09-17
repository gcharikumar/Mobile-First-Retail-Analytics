# docs/api.md

# Retail Insights API Documentation

Generated from FastAPI's OpenAPI spec at `/docs`.

## Endpoints
- **POST /api/v1/auth/token**: Login, returns JWT.
- **POST /api/v1/auth/consent**: Grant DPDP consent.
- **POST /api/v1/tenants**: Create tenant (super_user only).
- **GET /api/v1/tenants/{tenant_id}**: Get tenant details.
- **POST /api/v1/users**: Create user (owner only).
- **GET /api/v1/users/{user_id}**: Get user details.
- **POST /api/v1/pos/bills**: Create bill with line items.
- **GET /api/v1/analytics/top-products**: Top 5 products (week vs last week).
- **GET /api/v1/analytics/forecast**: Sales forecast (7 days).
- **POST /api/v1/whatsapp/alerts/low-stock**: Send low stock alert.

## Usage
Access via Swagger UI at `/docs` or export OpenAPI JSON for Postman.

## Authentication
- JWT (RS256) in `Authorization: Bearer <token>` header.
- RLS enforced via `tenant_id` in JWT payload.