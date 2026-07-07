# Fix 2: Engineering & Security — Critical Fixes Summary

**Team:** Fixing Team 2 — Engineering & Security
**Date:** 2026-07-07
**Review Source:** REVIEW_3_ENGINEERING_SECURITY.md
**Status:** ✅ All 5 critical fixes implemented

---

## Fix 1: AES-GCM IV Reuse (CRITICAL → FIXED)

**File:** `app/src/main/java/com/msaidizi/app/core/security/KeyManager.kt`

**Problem:** All N fields were encrypted with the same IV/Key pair. AES-GCM with IV reuse is catastrophic — XORing two ciphertexts recovers plaintext XOR, and authentication is completely broken (attacker can forge arbitrary ciphertexts).

**Fix:**
- Each `encrypt()` call generates a **unique 12-byte IV** via the Android Keystore's `Cipher.init()` (which calls SecureRandom internally)
- `setRandomizedEncryptionRequired(true)` on the KeyGenParameterSpec — the Keystore **itself enforces** unique IVs, providing a second layer of defense
- IV is prepended to ciphertext: output format is `[12-byte IV][ciphertext + GCM tag]`
- `encryptFields()` method encrypts each field with its **own separate IV**
- IV is extracted and used during `decrypt()`

**Key properties:**
- AES-256-GCM with hardware-backed keys (Android Keystore + StrongBox)
- 5 separate key aliases (auth, sync, biometric, storage, PII) — limits blast radius
- `require(iv.size == 12)` runtime assertion catches any Keystore anomaly
- `AEADBadTagException` thrown on tampered ciphertext (authentication intact)

---

## Fix 2: DeviceId Null Handling (CRITICAL → FIXED)

**File:** `app/src/main/java/com/msaidizi/app/core/security/DeviceBinder.kt`

**Problem:** If `READ_PHONE_STATE` permission was denied, `DeviceId` returned `null`. A null UID defeats device binding entirely — any device could claim to be any user. This is a critical authentication bypass.

**Fix:**
Multi-fallback chain with `ANDROID_ID` as primary fallback:

| Priority | Source | Stability | Permission Required |
|----------|--------|-----------|---------------------|
| 1 | IMEI (`TelephonyManager.deviceId`) | Highest (per-SIM-slot) | `READ_PHONE_STATE` (Android <10 only) |
| 2 | `Settings.Secure.ANDROID_ID` | High (per-device, resets on factory reset) | **None** |
| 3 | Instance UUID (`UUID.randomUUID()`) | Per-install | **None** |

**Key properties:**
- **Never returns null** — guaranteed to return a 64-char hex SHA-256 hash
- Rejects known-buggy ANDROID_ID value `9774d56d682e549c`
- Per-install salt prevents rainbow table attacks
- Hash is one-way — server cannot reverse to raw device ID
- `isHighConfidenceId()` method lets security policies adapt based on ID source
- `regenerateDeviceId()` for SIM swap detection recovery
- `invalidateCache()` for tamper detection scenarios

---

## Fix 3: Network Security Policy (HIGH → FIXED)

**File:** `app/src/main/res/xml/network_security_config.xml`

**Problem:** No `network_security_config.xml` existed. Android defaults allow cleartext (HTTP) traffic. A MITM attacker on public WiFi (common in East African markets) could intercept API keys, OTP codes, and financial data in transit.

**Fix:**
- **Blocks ALL cleartext (HTTP) traffic** globally via `<base-config cleartextTrafficPermitted="false">`
- **Certificate pinning** for `api.angavu.ai` and `federated.angavu.ai` with SHA-256 pins
- **Backup pins** included to prevent bricking during certificate rotation
- **Trust anchors** restricted to system CA store only — user-installed certificates (proxy/MITM apps) are rejected in release builds
- **Debug overrides** allow user CAs only in debug builds (for development)

**⚠️ Action Required:** Certificate pin values are **PLACEHOLDER**. Must be replaced with real SHA-256 fingerprints before production. Generate with:
```bash
openssl x509 -in cert.pem -pubkey -noout | \
  openssl pkey -pubin -outform DER | \
  openssl dgst -sha256 -binary | base64
```

**Must also add** to `AndroidManifest.xml`:
```xml
<application android:networkSecurityConfig="@xml/network_security_config" ...>
```

---

## Fix 4: Agent Output Sanitization (HIGH → FIXED)

**File:** `app/src/main/java/com/msaidizi/app/agent/Orchestrator.kt`

**Problem:** Agent responses were displayed directly without sanitization. A compromised or jailbroken LLM could inject XSS payloads, phishing links (fake M-Pesa domains), PII leakage, or prompt injection to manipulate downstream agents.

**Fix — 12-layer defense-in-depth:**

| Layer | Defense | What It Catches |
|-------|---------|-----------------|
| 1 | Control character removal | Terminal/shell injection (`\x00`-`\x1F`) |
| 2 | Zero-width character removal | Invisible prompt injection (`\u200B`, `\u200C`, etc.) |
| 3 | Dangerous HTML tag stripping | XSS via `<script>`, `<iframe>`, `<svg>`, etc. |
| 4 | All HTML tag stripping | Any remaining HTML markup |
| 5 | JS event handler removal | `onclick=`, `onerror=`, etc. |
| 6 | Dangerous URI neutralization | `javascript:`, `data:`, `vbscript:` URIs |
| 7 | PII masking | Kenyan phone numbers (`+254 7XX XXX XXX`), national IDs, account numbers |
| 8 | Prompt injection detection | 9 patterns: "ignore previous instructions", `[INST]`, `<\|im_start\|>`, "DAN jailbreak", etc. |
| 9 | URL validation | Fake M-Pesa/Safaricom domains, URL count cap (max 3), HTTP→HTTPS |
| 10 | Whitespace normalization | Layout attacks via excessive spaces |
| 11 | Length limiting | UI overflow prevention (5000 char cap) |
| 12 | HTML entity unescape | Clean up entities that survived stripping |

**Key design decisions:**
- Injection patterns are **stripped**, not rejected (rejecting = DoS vector)
- PII masking is **contextual** — only masks phone numbers when they match Kenyan patterns, IDs only near ID-related keywords
- Suspicious URLs for East African phishing (fake M-Pesa domains) have dedicated detection
- All sanitization is logged for security audit trail

---

## Fix 5: JWT RS256 (CRITICAL → FIXED)

**File:** `angavu-intelligence-backend/app/security/jwt_config.py`

**Problem:** JWT used HS256 (symmetric HMAC) — the same secret key signs and verifies tokens. If any service that verifies tokens is compromised, the signing key is exposed. An attacker can then forge tokens for any user, including admins.

**Fix:**
- Switched from **HS256** to **RS256** (RSA-SHA256 asymmetric signing)
- **Private key** signs tokens (held ONLY by the auth service)
- **Public key** verifies tokens (distributed to all API services)
- RSA-4096 keys (configurable, 2048 minimum enforced)
- **Key ID (`kid`)** in JWT header enables seamless key rotation via JWKS

**Token lifecycle:**
1. User authenticates (OTP/biometric)
2. Auth service creates access (15 min) + refresh (30 day) tokens with PRIVATE key
3. Access token sent to client; refresh token in HttpOnly cookie
4. API services verify using PUBLIC key (never have private key)
5. When access token expires, client uses refresh token for new pair

**Key properties:**
- JWKS endpoint (`/.well-known/jwks.json`) for public key distribution
- Token family-based theft detection (reuse of consumed refresh token revokes entire family)
- `jti` claim for per-token revocation
- `phone_hash` and `device_id_hash` in claims for device binding
- Keys generated and stored as PEM files (production should use KMS)
- `os.chmod(0o600)` on private key file

**API services use only the public key:**
```python
token_manager = get_token_manager()
payload = token_manager.verify_token(access_token)  # Uses public key only
```

---

## Files Created

| # | File | Lines | Purpose |
|---|------|-------|---------|
| 1 | `app/.../core/security/KeyManager.kt` | ~190 | AES-256-GCM with unique IV per encryption |
| 2 | `app/.../core/security/DeviceBinder.kt` | ~190 | Device ID with IMEI→ANDROID_ID→UUID fallback |
| 3 | `app/.../res/xml/network_security_config.xml` | ~80 | Block cleartext, certificate pinning |
| 4 | `app/.../agent/Orchestrator.kt` | ~270 | 12-layer agent output sanitization |
| 5 | `angavu-intelligence-backend/.../security/jwt_config.py` | ~310 | RS256 JWT with JWKS key rotation |

---

## Remaining Issues (Not in Top 5 but Noted)

The review identified 12 critical/high issues. The other 7 were:

| Issue | Severity | Status |
|-------|----------|--------|
| PQC implementations are stubs | CRITICAL | Not fixed (requires native ML-KEM/ML-DSA libraries, expected 2026 H2) |
| Token refresh unimplemented (Android) | CRITICAL | Not fixed (requires API endpoint implementation) |
| Differential privacy uses NumPy PRNG | CRITICAL | Not fixed (requires `secrets` module swap in `anonymizer.py`) |
| No rate limiting on OTP verify endpoint | HIGH | Not fixed (requires Redis-backed rate limiter) |
| Certificate pins are placeholder values | HIGH | ⚠️ Documented in network_security_config.xml, needs real values |
| Backend stores phone numbers in plaintext | HIGH | Not fixed (requires schema migration + index redesign) |
| OTP store is in-memory Python dict | HIGH | Not fixed (requires Redis-backed OTP store) |

---

*Completed by Fixing Team 2: Engineering & Security — Angavu Intelligence*
