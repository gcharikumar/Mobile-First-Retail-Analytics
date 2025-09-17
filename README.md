Retail Insights Grok

Mobile-first data insights platform for retail with multi-tenancy, POS, analytics, and WhatsApp integration. Built with FastAPI, Flutter, React (PWA), and Prefect.

## Features
- Multi-tenant core with Row-Level Security (RLS)
- POS/billing, inventory tracking (offline-first)
- Data ingestion (CSV/Excel/Google Sheets) with validation
- Analytics: Top products, forecasting, NLP for product unification
- WhatsApp integration: Daily pulse, low stock alerts
- Localized UI: English, Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam
- DPDP compliance: Consent, data residency (AWS Mumbai), audit logs
- CI/CD with GitHub Actions, testing (pytest, Flutter test, Vitest)

## Setup
1. **Clone repo**: `git clone <repo> && cd retail-insights-monorepo`
2. **Install deps**:
   - Backend: `pip install -r backend/requirements.txt`
   - Mobile: `cd mobile && flutter pub get`
   - Frontend: `cd frontend && npm install`
3. **Copy env**: `cp .env.example .env` and fill values (e.g., `DATABASE_URL`, `JWT_SECRET`)
4. **Run local stack**: `docker-compose up -d`
5. **Apply migrations**: `cd backend && alembic upgrade head`
6. **Seed data**: `python scripts/seed_db.py`
7. **Run backend**: `cd backend && uvicorn app.main:app --reload`
8. **Run mobile**: `cd mobile && flutter run`
9. **Run frontend**: `cd frontend && npm run dev`
10. **Run ETL**: `cd etl && prefect server start && prefect deployment apply prefect.yaml`

## Testing
- Backend: `cd backend && pytest`
- Mobile: `cd mobile && flutter test`
- Frontend: `cd frontend && npm run test`
- E2E: Use Playwright (`tests/e2e/`) or Postman collection (from `/docs`)

## Deployment
- Push to `main` triggers GitHub Actions CI/CD
- Deploy backend to AWS ECS, PWA to S3, mobile to S3 (APK/IPA)
- Run `./scripts/deploy.sh` for manual deployment

## DPDP Compliance
- Consent: Required for customer phone (UI/API)
- Data residency: AWS Mumbai region
- Audit logs: Stored in `audits` table
- Retention: 365 days (configurable)
- Erasure: Soft delete via `is_deleted`

## Directory Structure