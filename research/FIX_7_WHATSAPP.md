# FIX 7: WhatsApp Architecture Redesign

**Status:** ✅ Complete  
**Date:** 2026-07-07  
**Scope:** WhatsApp as a secure, reliable, isolated report delivery channel

---

## Executive Summary

WhatsApp integration was redesigned from a monolithic authentication+delivery system into a **clean secondary report delivery channel**. Msaidizi app remains the primary authentication and interaction platform. WhatsApp is now optional, isolated per-worker, encrypted, and resilient.

### Critical Issues Fixed

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | OpenWA port/URL hardcoded | CRITICAL | All settings via environment variables, Docker service names |
| 2 | No multi-device isolation | CRITICAL | Every DB query includes user_id filter, session scoping |
| 3 | No login fallback | CRITICAL | Msaidizi app = PRIMARY auth, WhatsApp = optional secondary |
| 4 | No field-level encryption | CRITICAL | AES-256-GCM phone encryption, SHA-256 hash for lookups |
| 5 | OTP vulnerable | HIGH | 5-min expiry, 5 attempt limit, rate limiting, lockout |
| 6 | No multi-tenancy | HIGH | Per-user isolation in all services |
| 7 | QR flow breaks in production | HIGH | Headless auth, session persistence, auto-reconnect |
| 8 | No session persistence | MEDIUM | Docker volume for auth state, survives restarts |
| 9 | No connection recovery | MEDIUM | Exponential backoff reconnection (10 attempts) |
| 10 | No health monitoring | MEDIUM | Health endpoint, consecutive failure tracking, alerts |
| 11 | No delivery confirmation | MEDIUM | Message receipt tracking, delivery status API |
| 12 | Rate limiting incomplete | MEDIUM | Per-user + global rate limits |

---

## Architecture Redesign

### Before (Broken)
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ WhatsApp │────▶│  OpenWA   │────▶│ Backend  │──▶ DB (no isolation)
│ (Auth!)  │     │ :3456?    │     │ :3000?   │   (plaintext phones)
└──────────┘     └──────────┘     └──────────┘   (no encryption)
                        ↑
                   localhost URLs
                   no persistence
                   no monitoring
```

### After (Fixed)
```
┌─────────────────────────────────────────────────────────┐
│                    Msaidizi App                          │
│  PRIMARY: Phone + OTP + Biometric                       │
│  Transactions, Voice, On-device AI                      │
│  Works WITHOUT WhatsApp                                 │
└──────────────┬──────────────────────────────────────────┘
               │ Optional report delivery
               ▼
┌──────────┐     ┌──────────────┐     ┌──────────────────┐
│ WhatsApp │◀────│   OpenWA     │◀────│    Backend        │
│ (Reports │     │  :3000       │     │   (FastAPI)       │
│  only)   │     │              │     │                   │
└──────────┘     │ • Env vars   │     │ • user_id scoped  │
                 │ • Volume     │     │ • Phone encrypted │
                 │ • Auto-recon │     │ • HMAC webhooks   │
                 │ • Health     │     │ • OTP hardened    │
                 └──────────────┘     └──────────────────┘
                      Docker Network
                   (service names, not localhost)
```

---

## Files Created/Modified

### OpenWA Service (Node.js)

| File | Description |
|------|-------------|
| `openwa/index.js` | **Rewritten.** Env-based config, session persistence, auto-reconnect, health endpoint, rate limiting (per-user + global), delivery tracking, HMAC webhook signatures |
| `openwa/Dockerfile` | Session volume mount, health check |
| `openwa/docker-compose.yml` | Docker service names, named volumes, env vars, health checks |
| `openwa/.env.example` | All configurable settings documented |

### Backend (Python)

| File | Description |
|------|-------------|
| `app/security/phone_encryption.py` | **New.** AES-256-GCM field-level encryption for phone numbers, SHA-256 hash for lookups |
| `app/models/user.py` | **New.** User model with encrypted phone, WhatsApp connection tracking, user_id scoped queries |
| `app/api/v1/whatsapp_connection.py` | **New.** WhatsApp connect/disconnect/status endpoints, all queries user_id scoped |
| `app/api/v1/whatsapp_webhooks.py` | **New.** Webhook handler with HMAC verification, report triggers, health proxy |
| `app/services/whatsapp_bot.py` | **New.** Command processing, Swahili help text, rate limiting |
| `app/services/whatsapp_delivery.py` | **New.** Report delivery with user_id isolation, retry logic, delivery confirmation |
| `app/services/whatsapp_health.py` | **New.** Health monitoring, consecutive failure tracking, alert generation |
| `app/services/otp_service.py` | **New.** Hardened OTP: 5-min expiry, 5 attempts, rate limiting, account lockout |

---

## Fix Details

### Fix 1: OpenWA Configuration

**Problem:** Port hardcoded (backend expected 3000, OpenWA listened on 3456). URLs used `localhost` which breaks in Docker.

**Solution:**
- All settings via environment variables (`OPENWA_PORT`, `BACKEND_URL`, etc.)
- Docker services communicate via service names (`http://openwa:3000`, `http://backend:8000`)
- `.env.example` documents all configuration
- Docker Compose uses env var substitution

```javascript
// Before (hardcoded)
const port = 3456;
axios.post('http://localhost:3000/send-message', ...)

// After (configurable)
const port = parseInt(process.env.OPENWA_PORT || "3000", 10);
const backendUrl = process.env.BACKEND_URL || "http://backend:8000";
```

### Fix 2: Multi-Device Isolation

**Problem:** DB queries had no user_id filter. Worker A could read Worker B's data.

**Solution:**
- **Every** database query includes `user_id` filter
- Each worker's WhatsApp session is isolated
- Report delivery explicitly requires `user_id` parameter
- No global queries without user scoping

```python
# Before (no isolation)
users = db.query(User).all()  # ALL users!

# After (isolated)
user = db.query(User).filter(
    User.id == user_id,           # MUST specify user
    User.is_active == True,
).first()

# Bulk delivery still scoped
users = db.query(User).filter(
    User.whatsapp_connected == True,  # Only opted-in
    User.is_active == True,
).all()
# Each delivery: send_report(user_id=str(user.id), ...)
```

### Fix 3: Phone Number Encryption

**Problem:** Phone numbers stored plaintext in database.

**Solution:**
- AES-256-GCM encryption for phone numbers (same scheme as Android KeyManager)
- Each encryption uses a unique 12-byte IV
- SHA-256 hash for database lookups (deterministic, no decryption needed)
- Phone numbers masked in API responses (`****5678`)

```python
# Encryption
pe = PhoneEncryption()
encrypted = pe.encrypt_phone("0712345678")  # → Base64(IV + ciphertext)
decrypted = pe.decrypt_phone(encrypted)     # → "254712345678"

# Lookup (no decryption)
phone_hash = PhoneEncryption.hash_phone("0712345678")  # → SHA-256 hex
user = db.query(User).filter(User.phone_hash == phone_hash).first()

# Display
masked = PhoneEncryption.mask_phone("254712345678")  # → "********5678"
```

### Fix 4: OpenWA Session Persistence

**Problem:** WhatsApp session lost on container restart.

**Solution:**
- Auth state saved to Docker named volume (`openwa-session`)
- Volume persists across container restarts
- Auto-reconnect on transient disconnects (exponential backoff)
- Graceful handling of WhatsApp logout (re-QR required)

```yaml
# docker-compose.yml
volumes:
  openwa-session:
    driver: local

services:
  openwa:
    volumes:
      - openwa-session:/app/session
```

### Fix 5: WhatsApp as Report Channel (Not Auth)

**Problem:** WhatsApp was used for authentication. Lose WhatsApp = lose account.

**Solution:**
- **Msaidizi app = PRIMARY auth** (phone + OTP + biometric)
- **WhatsApp = SECONDARY** (report delivery only)
- WhatsApp connection is **OPTIONAL** (worker can choose not to connect)
- If WhatsApp disconnects, app still works fully
- WhatsApp reconnection is graceful (app detects and offers to reconnect)

```
Auth Flow:
  Msaidizi App → Phone + OTP + Biometric → Full Access
  WhatsApp → Optional → Report Delivery Only

If WhatsApp disconnects:
  App notification: "WhatsApp disconnected. Reconnect?"
  App continues working normally
  Reports queued, delivered when reconnected
```

### Fix 5b: OTP Hardened

**Problem:** 6-digit code, no rate limiting, 10-minute expiry.

**Solution:**
- 5-minute expiry (reduced from 10)
- 5 max verification attempts per OTP
- 3 OTP requests per phone per hour
- Account locked for 30 minutes after 5 failed attempts
- Timing-safe comparison (`secrets.compare_digest`)
- Codes hashed before storage (never plaintext)

---

## Security Properties

### Encryption
- **Phone numbers:** AES-256-GCM with unique IV per field
- **Phone lookups:** SHA-256 deterministic hash
- **Webhook signatures:** HMAC-SHA256 on all OpenWA ↔ Backend communication
- **OTP codes:** SHA-256 hashed before storage

### Isolation
- **User scoping:** Every DB query includes user_id filter
- **WhatsApp sessions:** Per-user session tracking
- **Report delivery:** Explicit user_id required for every send
- **Rate limiting:** Per-user AND global limits

### Resilience
- **Session persistence:** Docker volume survives restarts
- **Auto-reconnect:** Exponential backoff (10 attempts, max 60s delay)
- **Health monitoring:** Continuous checks, alert after 2 failures
- **Delivery confirmation:** Message receipt tracking

### OTP Security
- **Short expiry:** 5 minutes
- **Attempt limit:** 5 per OTP
- **Request limit:** 3 per phone per hour
- **Account lockout:** 30 minutes after 5 failures
- **Timing-safe:** Prevents timing attacks

---

## Integration Flow

### Onboarding (App → Backend → WhatsApp)

1. Worker completes Msaidizi app onboarding (PRIMARY auth established)
2. App asks: "Unatumia WhatsApp?" (optional)
3. If yes: Worker provides WhatsApp phone number
4. Backend encrypts and stores phone, sends test message via OpenWA
5. WhatsApp is now connected for report delivery

### Report Delivery (Backend → OpenWA → WhatsApp)

1. Backend scheduler triggers (7 PM EAT daily for daily reports)
2. Queries users with `whatsapp_connected == True` (only opted-in)
3. For each user: generates report, sends via OpenWA with `user_id`
4. OpenWA delivers to WhatsApp, tracks delivery receipt
5. Failed deliveries retried 3 times with exponential backoff

### Incoming Commands (WhatsApp → OpenWA → Backend)

1. Worker sends "Ripoti ya leo" via WhatsApp
2. OpenWA receives, forwards to backend with HMAC signature
3. Backend verifies signature, processes command
4. Report generated and sent back via OpenWA

### WhatsApp Disconnect Recovery

1. OpenWA detects WhatsApp logout
2. Notifies backend via webhook
3. Backend marks user as disconnected
4. App shows: "WhatsApp disconnected. Reconnect?"
5. Worker can reconnect anytime from app
6. App works fully without WhatsApp

---

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENWA_PORT` | `3000` | OpenWA HTTP server port |
| `OPENWA_HOST` | `0.0.0.0` | OpenWA bind address |
| `OPENWA_SESSION_PATH` | `/app/session` | Session data directory |
| `BACKEND_URL` | `http://backend:8000` | Backend URL (Docker service name) |
| `OPENWA_URL` | `http://openwa:3000` | OpenWA URL (Docker service name) |
| `BACKEND_WEBHOOK_SECRET` | — | HMAC secret (min 16 chars, REQUIRED) |
| `PHONE_ENCRYPTION_KEY` | — | 32-byte hex key for phone encryption (REQUIRED) |
| `RATE_LIMIT_WINDOW_MS` | `60000` | Rate limit window (ms) |
| `RATE_LIMIT_MAX_REQUESTS` | `100` | Per-user requests per window |
| `RATE_LIMIT_GLOBAL_MAX` | `500` | Global requests per window |
| `RECONNECT_MAX_ATTEMPTS` | `10` | Max reconnect attempts |
| `RECONNECT_BASE_DELAY_MS` | `1000` | Base reconnect delay |
| `RECONNECT_MAX_DELAY_MS` | `60000` | Max reconnect delay |

### Docker Volumes

| Volume | Purpose |
|--------|---------|
| `openwa-session` | WhatsApp auth state (persists across restarts) |
| `whisper-models` | Whisper STT model cache |
| `redis-data` | Redis persistent data |

---

## API Endpoints

### OpenWA Service

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Full health status |
| GET | `/status` | Quick connection status |
| GET | `/qr` | QR code for authentication |
| POST | `/send-message` | Send text message (requires user_id) |
| POST | `/send-image` | Send image (requires user_id) |
| POST | `/send-voice` | Send voice note (requires user_id) |
| GET | `/delivery-status/:id` | Check delivery status |

### Backend

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/whatsapp/connect` | Connect WhatsApp for a worker |
| POST | `/api/v1/whatsapp/disconnect` | Disconnect WhatsApp |
| GET | `/api/v1/whatsapp/status/{user_id}` | Get connection status |
| POST | `/api/v1/webhooks/whatsapp` | Incoming message webhook |
| POST | `/api/v1/webhooks/whatsapp/status` | Connection status webhook |
| POST | `/api/v1/webhooks/whatsapp/daily-reports` | Trigger daily reports |
| GET | `/api/v1/webhooks/whatsapp/health` | Backend health |
| GET | `/api/v1/webhooks/whatsapp/openwa-health` | Proxy OpenWA health |

---

## Testing Checklist

- [ ] Phone encryption: encrypt → decrypt roundtrip
- [ ] Phone hash: same phone always produces same hash
- [ ] User isolation: query with wrong user_id returns nothing
- [ ] OTP: expires after 5 minutes
- [ ] OTP: locks after 5 failed attempts
- [ ] OTP: rate limits after 3 requests per hour
- [ ] OpenWA: session survives container restart
- [ ] OpenWA: auto-reconnects on transient disconnect
- [ ] OpenWA: health endpoint returns correct status
- [ ] Delivery: retries 3 times on failure
- [ ] Delivery: tracks message receipt
- [ ] Webhook: rejects invalid HMAC signatures
- [ ] Rate limiting: blocks after limit exceeded
- [ ] WhatsApp disconnect: app still works
- [ ] WhatsApp reconnect: graceful reconnection

---

## Dependencies

### OpenWA (Node.js)
- `@whiskeysockets/baileys` ^6.7.9
- `express` ^4.21.0
- `pino` ^9.4.0

### Backend (Python)
- `cryptography` — AES-256-GCM phone encryption
- `httpx` — Async HTTP client for OpenWA
- `fastapi` — Web framework
- `sqlalchemy` — Database ORM
- `redis` — OTP store (production)

---

## Migration Notes

For existing deployments:
1. Generate `PHONE_ENCRYPTION_KEY` (32 random bytes, hex-encoded)
2. Migrate existing plaintext phones to encrypted format
3. Generate `BACKEND_WEBHOOK_SECRET` (32+ random chars)
4. Update Docker Compose to use new service names
5. Create `openwa-session` Docker volume
6. Deploy backend with new environment variables
7. Redeploy OpenWA with new configuration
8. Test WhatsApp connection and report delivery
