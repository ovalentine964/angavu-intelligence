# Engineering & Security Review

**Reviewer:** Review Team 3 — Engineering & Security  
**Date:** 2026-07-07  
**Scope:** `msaidizi-app` (Android/Kotlin) + `angavu-intelligence-backend` (Python/FastAPI)  
**Threat Model:** Livelihood data of informal workers across East Africa. Adversaries include SIM-swap fraudsters, state-level surveillance, and data brokers.

---

## Engineering

### Strengths

- **Well-structured Android architecture.** Clean separation of concerns: `security/`, `agent/`, `voice/`, `ui/`, `core/`. Hilt DI is used consistently. Room database with SQLCipher for encrypted-at-rest storage.
- **Comprehensive input validation.** `InputSanitizer.kt` covers SQL injection, XSS, and prompt injection patterns. `ApiValidator.kt` validates JSON structure, numeric ranges, and sanitizes against prototype pollution.
- **Robust CI/CD pipeline (Android).** `ci.yml` has lint (Detekt) → unit tests → build → security scan → release build. APK size checks. Build logs uploaded on failure.
- **Backend CI is solid.** `test.yml` runs ruff lint, mypy type checking, and pytest with real PostgreSQL + Redis services. Coverage reporting included.
- **Extensive dialect support.** 15+ dialect adapters (Swahili, Dholuo, Kikuyu, Hausa, Yoruba, Zulu, etc.) with dedicated data files. This is genuine domain expertise.
- **Federated learning architecture is well-designed.** Privacy guarantees are documented, differential privacy parameters are correct (ε=1.0, δ=1e-5), FedAvg aggregation is properly implemented with quality validation and rollback on degradation.
- **ProGuard/R8 configured.** Release builds have minification, shrinkResources, and comprehensive keep rules for Room, Hilt, serialization, ONNX, and native methods.
- **Backend config validation.** `config.py` uses pydantic validators that reject default/empty secrets in production. Minimum length enforcement for JWT_SECRET_KEY (32 chars), ENCRYPTION_KEY, etc.
- **Database encryption on Android.** SQLCipher (`net.zetetic:android-database-sqlcipher:4.5.4`) is included for Room database encryption at rest.
- **Token storage is properly secured.** `SecureTokenStorage.kt` uses `EncryptedSharedPreferences` backed by Android Keystore with StrongBox preference.

### Issues

- **[CRITICAL] All PQC (Post-Quantum Cryptography) implementations are STUBS.** `MlKemProvider.kt`, `MlDsaProvider.kt`, `HybridKeyExchange.kt` (Android) and `ml_kem.py`, `ml_dsa.py`, `hybrid_key_exchange.py` (backend) all generate random bytes instead of performing actual cryptographic operations. `MlDsaProvider.verify()` always returns `true`. If any code path depends on PQC for security, it provides zero protection. — `msaidizi-app:security/crypto/pqc/MlDsaProvider.kt:119`, `angavu-intelligence-backend:app/security/pqc/ml_dsa.py:85`

- **[CRITICAL] Token refresh is not implemented (Android).** `JwtTokenManager.refreshToken()` returns `null` with a `// TODO: Replace with actual API call` comment. Users will be logged out after 15 minutes with no way to refresh. — `msaidizi-app:security/auth/JwtTokenManager.kt:134`

- **[HIGH] Certificate pins are placeholder values.** Both `TlsConfig.kt` and `PinnedHttpClient.kt` use `sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=` placeholder pins. Certificate pinning is effectively disabled even in release builds. `network_security_config.xml` also has a TODO pin. — `msaidizi-app:security/crypto/TlsConfig.kt:40-41`, `msaidizi-app:core/network/PinnedHttpClient.kt:56-57`

- **[HIGH] Backend OTP store is in-memory Python dict.** `_otps: dict = {}` in `otp_auth.py`. All pending OTPs are lost on server restart. No persistence, no Redis backing despite Redis being configured. For a phone auth system serving potentially thousands of concurrent users, this is fragile. — `angavu-intelligence-backend:app/api/otp_auth.py:37`

- **[HIGH] Backend schema stores phone numbers in plaintext.** `database/schema.sql` defines `phone VARCHAR(20)` across `users`, `whatsapp_connections`, `verifications`, and `whatsapp_messages` tables. While the Python code encrypts via `encrypt_value()`, the raw schema allows plaintext storage and the index `idx_users_phone` indexes the raw phone column. — `angavu-intelligence-backend:database/schema.sql:6,21,37,118`

- **[HIGH] Backend Dockerfile runs as root.** No `USER` directive. Container runs as root by default, violating container security best practices. — `angavu-intelligence-backend:Dockerfile`

- **[MEDIUM] CI security scan is a no-op.** The Android `ci.yml` security job just prints "Security scan complete" without actually running OWASP dependency-check, Snyk, or any vulnerability scanner. — `msaidizi-app:.github/workflows/ci.yml:85-91`

- **[MEDIUM] 50+ TODO/FIXME items across both repos.** Key incomplete items: `ModelRouter.kt:1234` (empty list stub), `SyncManager.kt:243` (remote changes not applied), `BusinessDiscoveryFragment.kt:394` (not saved to DB), `ModelDownloadManager.kt:188,233` (not integrated), `self_evolution.py:204` (no DB persistence), `self_evolution.py:529` (no analytics wiring).

- **[MEDIUM] Code duplication in dialect adapters.** 11 dialect adapters (`HausaDialectAdapter`, `IgboDialectAdapter`, `KalenjinDialectAdapter`, etc.) all have `TODO(refactor): Migrate to data-driven DialectAdapter base class`. This suggests copy-paste architecture.

- **[MEDIUM] Backend has two test directories with overlapping scope.** `tests/autonomous/` and `tests/test_autonomous/` both test the autonomous subsystem. This creates confusion about which is canonical.

- **[LOW] `mypy` is non-blocking in CI.** The type check step uses `|| true`, meaning type errors don't fail the build. This weakens the value of static analysis. — `angavu-intelligence-backend:.github/workflows/test.yml:49`

- **[LOW] Android build uses `cp` in CI to switch build files.** The KSP migration is done by copying `build.gradle.ksp` → `build.gradle.kts` in CI. This is fragile and should be a proper Gradle configuration toggle. — `msaidizi-app:.github/workflows/ci.yml:33-35`

---

## Security

### Strengths

- **OTP implementation is well-designed (Android).** `OtpManager.kt` has: 6-digit OTP via `SecureRandom`, SHA-256 hashed storage, 5-minute expiry, rate limiting (3/10min, 10/hour), attempt limiting (5 failures → 15min lockout, 10 → freeze), anti-enumeration (consistent responses), and single-use invalidation.

- **Biometric auth properly uses Android Keystore/TEE.** `BiometricAuthManager.kt` uses `BIOMETRIC_STRONG` authenticator, supports crypto-bound biometric via `authenticateWithCrypto()`, and delegates to TEE/StrongBox via the system biometric API.

- **AES-256-GCM encryption at rest (Android).** `KeyManager.kt` generates hardware-backed keys in Android Keystore with `setRandomizedEncryptionRequired(true)`, prefers StrongBox, and uses proper IV handling (12 bytes prepended to ciphertext). Separate key aliases for auth, sync, biometric, storage, and DB.

- **Backend encryption is solid.** `crypto.py` uses AES-256-GCM with PBKDF2 key derivation (480,000 iterations per OWASP), random salt per encryption, and 96-bit nonces. HMAC-SHA256 for webhook verification with constant-time comparison.

- **Refresh token rotation with family-based theft detection (backend).** `auth.py` implements proper token families: each refresh is single-use, reuse of a consumed token revokes the entire family. This prevents token replay attacks.

- **SIM swap detection is comprehensive.** `SuspiciousLoginDetector.kt` implements a multi-factor risk scoring engine with weighted signals (SIM change 40%, new device 15%, unusual location 15%, unusual time 10%, velocity spike 10%, failed biometric 10%). 48-hour cooling period after SIM change. Graduated response from ALLOW → FREEZE_ACCOUNT.

- **Federated learning preserves privacy.** Raw audio/text never leaves device. Only anonymized correction patterns (hashed n-grams, phoneme confusion patterns) are shared. Differential privacy (ε=1.0) applied before aggregation. Device ID is a one-way hash with per-installation salt.

- **Anonymization pipeline is thorough (backend).** `anonymizer.py` implements 4-layer privacy architecture: raw → pseudonymized → k-anonymity (k≥10) → aggregated. Product generalization hierarchy. Temporal minimum enforcement (ward-level requires weekly aggregation). Full audit logging of data access.

- **Consent management covers all regulatory requirements.** `ConsentManager.kt` has 10 separate consent purposes (service core, KYC, biometric face/voice, financial data, analytics, marketing, credit scoring, third-party sharing, location) with timestamps and withdrawal tracking per DPA/NDPA/POPIA/GDPR.

- **Data minimization is implemented.** `DataMinimizer.kt` strips PII for ML training, generalizes location to region, replaces exact timestamps with time bins, and hashes user IDs for analytics. `anonymizer.py` has field-level allowlists per export purpose.

- **TLS 1.3 enforcement.** `TlsConfig.kt` configures TLSv1.3 with TLSv1.2 fallback. HTTPS-only interceptor blocks cleartext. Security headers (X-Content-Type-Options, X-Request-ID) added via OkHttp interceptor.

- **LLM output sanitization.** `InputSanitizer.sanitizeLlmOutput()` masks phone numbers, national IDs, account numbers, internal API endpoints, and database schema info in LLM responses before showing to users.

### Vulnerabilities

- **[CRITICAL] JWT uses HS256 (symmetric) instead of RS256 (asymmetric).** The security architecture spec calls for RS256, but `config.py` defaults to `HS256`. With HS256, the same secret key is used for signing and verification. If any service that verifies tokens is compromised, the signing key is exposed. For a system with a backend API and potentially multiple services, RS256 is essential. — `angavu-intelligence-backend:app/config.py:41`

- **[CRITICAL] ML-DSA verification always returns True.** `MlDsaProvider.verify()` (both Kotlin and Python) is a stub that returns `true` unconditionally. Any code path relying on signature verification (document signing, update integrity) will accept forged signatures. — `msaidizi-app:security/crypto/pqc/MlDsaProvider.kt:119`, `angavu-intelligence-backend:app/security/pqc/ml_dsa.py:85`

- **[CRITICAL] Differential privacy uses non-cryptographic RNG (backend).** `anonymizer.py:223,255` uses `np.random.laplace()` and `np.random.normal()` which use NumPy's PRNG (Mersenne Twister), not cryptographically secure randomness. An attacker who can observe multiple noised outputs could potentially reconstruct the PRNG state and reverse the noise. The Android client correctly uses `SecureRandom`. — `angavu-intelligence-backend:app/services/anonymizer.py:223,255`

- **[HIGH] No rate limiting on OTP verification endpoint.** `otp_auth.py` rate-limits OTP *requests* (3/10min) but has NO rate limiting on `verify_otp`. An attacker with a valid phone number can brute-force the 6-digit OTP (1M combinations) without any lockout. The Android client has this (5 attempts → lockout), but the server doesn't enforce it. — `angavu-intelligence-backend:app/api/otp_auth.py:verify_otp`

- **[HIGH] Backend OTP verification doesn't check attempt count.** The server-side verify endpoint iterates through all stored OTPs for a phone and checks if any match. There's no per-phone attempt counter or lockout. Combined with the in-memory store, this is a brute-force vector. — `angavu-intelligence-backend:app/api/otp_auth.py:140-155`

- **[HIGH] Database schema has unencrypted PII columns.** `schema.sql` stores `phone VARCHAR(20)`, `user_name VARCHAR(100)`, and `code VARCHAR(10)` (OTP) in plaintext. While the Python code uses `encrypt_value()`, the schema itself allows plaintext and the indexes (`idx_users_phone`, `idx_whatsapp_connections_phone`) index raw values. Any SQL injection or direct DB access exposes PII. — `angavu-intelligence-backend:database/schema.sql:6,21,37`

- **[HIGH] `DATA_ENCRYPTION_SALT` has a hardcoded default.** `config.py:57` defaults to `"msaidizi-salt-2026"`. While the validator doesn't reject it (unlike SECRET_KEY), this is a static salt used across all deployments. If the salt is the same in dev and prod, hashed values are portable. — `angavu-intelligence-backend:app/config.py:57`

- **[MEDIUM] Federated learning update signature verification is trivial.** `_verify_update_signature()` in `federated_learning.py` only checks device ID length (>8 chars) and timestamp freshness (<24h). No cryptographic signature verification. A malicious client could inject poisoned updates with fabricated device IDs. — `angavu-intelligence-backend:app/services/federated_learning.py:_verify_update_signature`

- **[MEDIUM] Session timeout state is in-memory only (Android).** `SessionManager.kt` uses a plain `Thread` for session monitoring and `MutableStateFlow` for state. If the process is killed, session state is lost. The 5-minute timeout is enforced client-side only — the backend has no session timeout enforcement. — `msaidizi-app:security/auth/SessionManager.kt`

- **[MEDIUM] Consent stored in SharedPreferences (not encrypted).** `ConsentManager.kt` uses plain `SharedPreferences` for consent records. While consent status itself isn't highly sensitive, the timestamps and withdrawal records should be tamper-evident for regulatory compliance. An attacker with root access could modify consent records. — `msaidizi-app:security/privacy/ConsentManager.kt:40`

- **[MEDIUM] Audit log files are not integrity-protected.** `CryptoAuditLogger.kt` writes JSONL files without any HMAC or chain hash. An attacker who gains file access could modify or delete audit entries without detection. The "tamper-evident" claim in the docstring is not implemented. — `msaidizi-app:security/crypto/pqc/CryptoAuditLogger.kt`

- **[MEDIUM] Backend `Secret` field in `verifications` table stores OTP codes.** The `code VARCHAR(10)` column in `verifications` stores OTP codes. If these aren't cleared after verification, they persist in the database. The schema has no TTL or cleanup mechanism. — `angavu-intelligence-backend:database/schema.sql:37`

- **[LOW] `InputSanitizer` prompt injection patterns are easily bypassed.** The patterns use simple regex that can be circumvented with Unicode homoglyphs, zero-width characters, or creative spacing. For example, "ign〇re previ〇us instructi〇ns" would bypass the pattern. This is a known limitation of regex-based prompt injection detection. — `msaidizi-app:security/validation/InputSanitizer.kt:33-44`

- **[LOW] ProGuard strips `Log.d` and `Log.v` in release builds.** `proguard-rules.pro:103-106` removes debug/verbose Android logs. If any security audit logging goes through `Log.d()`, it will be silently removed in release builds. Timber's debug calls would also be affected if Timber delegates to `Log.d`. — `msaidizi-app:app/proguard-rules.pro:103-106`

---

## Verdict: NEEDS WORK

### Summary

The codebase demonstrates strong **security architecture design** — the OTP flow, biometric auth, encryption at rest, federated learning privacy, consent management, and anonymization pipeline are all well-conceived and properly documented. The team clearly understands the threat model for informal workers' livelihood data.

However, **implementation has critical gaps**:

1. **PQC is entirely non-functional** (all stubs, verify returns true)
2. **JWT uses HS256 instead of RS256** (spec says RS256, code says HS256)
3. **Token refresh is unimplemented** (15-minute forced logout)
4. **Backend OTP has no brute-force protection** on verify endpoint
5. **Differential privacy uses non-cryptographic RNG** (NumPy PRNG)
6. **Certificate pins are placeholders** (pinning effectively disabled)

### Must-Fix Before Production

| # | Issue | Severity | Effort |
|---|-------|----------|--------|
| 1 | Switch JWT to RS256 | CRITICAL | 1-2 days |
| 2 | Add rate limiting to OTP verify endpoint | HIGH | 1 day |
| 3 | Replace placeholder certificate pins | HIGH | 1 day |
| 4 | Implement token refresh flow | CRITICAL | 2-3 days |
| 5 | Switch `np.random` to `secrets` in anonymizer | CRITICAL | 1 hour |
| 6 | Encrypt PII columns in database schema | HIGH | 2-3 days |
| 7 | Add non-root user to Dockerfile | HIGH | 10 minutes |
| 8 | Make PQC stubs fail loudly (throw, not silently succeed) | CRITICAL | 1 hour |

### Architecture is Sound, Execution Has Gaps

The security architecture document is excellent. The gap between design and implementation is the primary risk. The team should prioritize closing the 8 must-fix items above before any production deployment. The PQC stubs are acceptable for a pre-production prototype *only if* they are clearly feature-flagged and not reachable by production code paths — but `verify() → true` is dangerous regardless.
