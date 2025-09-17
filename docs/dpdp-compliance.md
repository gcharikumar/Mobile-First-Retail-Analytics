# docs/dpdp-compliance.md

# DPDP Compliance Checklist

Ensures compliance with India's Digital Personal Data Protection Act 2023.

## Requirements
- **Consent**: Granular, revocable consent for customer phone (UI: `ConsentScreen`, `ConsentModal`; API: `/auth/consent`).
- **Data Minimization**: Hash phone numbers (`security.py` uses Argon2).
- **Data Residency**: AWS Mumbai region (set in `.env`, `deploy.sh`).
- **Right to Erasure**: Soft delete (`is_deleted` in models).
- **Audit Logs**: Stored in `audits` table, no PII in details.
- **Retention**: 365 days, configurable via `DATA_RETENTION_DAYS`.
- **Opt-in for WhatsApp**: Alerts/pulse sent only with consent (`whatsapp.py`).

## Implementation
- Consent UI in Flutter (`consent_screen.dart`) and React (`ConsentModal.jsx`).
- Consent API in FastAPI (`auth.py`).
- Hashed phone storage in `users`, `customers`, `bills` models.
- Audit logs via `audit.py`, logged in `logging.py`.
- Mumbai region enforced in `docker-compose.yml`, `deploy.sh`.

## Verification
- Test consent flow: `pos_test.dart`, `pos_form.test.jsx`.
- Check logs: `logs/app-*.log` (JSON format).
- Validate residency: AWS CLI (`aws configure`).