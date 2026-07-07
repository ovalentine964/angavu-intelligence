# Implementation 15: Multi-Channel Gateway (OpenClaw Pattern)

**Date:** 2026-07-07
**Status:** ✅ Core implementation complete
**Swarm:** Impl 15 — Multi-Channel Gateway

---

## Problem

Angavu's channels are SEPARATE — Msaidizi app (voice + text) and WhatsApp (via OpenWA) don't share sessions or memory. A worker who starts a conversation on the app and switches to WhatsApp loses all context. The "AI CFO" resets.

## Solution: OpenClaw Pattern

**One agent system, multiple channels, same session.**

OpenClaw proves this works at scale: ONE Gateway process serves 20+ messaging platforms with unified sessions and memory. We adapt this pattern for Angavu's 4 channels.

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Msaidizi   │    │  WhatsApp   │    │   SMS/      │    │   Voice     │
│  App        │    │  (OpenWA)   │    │   USSD      │    │   Calls     │
│  (voice+text)│    │             │    │             │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Channel Adapters (normalize)                      │
│   AppAdapter  │  WhatsAppAdapter  │  SMSAdapter  │  VoiceAdapter    │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│              Multi-Channel Gateway (central router)                  │
│                                                                      │
│  1. Receive UnifiedMessage from any channel                          │
│  2. Resolve worker identity → canonical user_id                      │
│  3. Get/create session (SAME session across channels)                │
│  4. Route to Intelligence Pipeline                                   │
│  5. Save to session history                                          │
│  6. Return response through source channel                           │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Session Sync (SQLite)                             │
│                                                                      │
│  • Sessions keyed by WORKER, not by CHANNEL                          │
│  • Conversation history preserved across channel switches            │
│  • Context (topic, variables) carries over                           │
│  • Channel usage statistics                                          │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│               Intelligence Pipeline (existing)                       │
│                                                                      │
│  IntentRouter → Agent Selection → Analysis → Response                │
│  Same pipeline, regardless of which channel the message came from.   │
└──────────────────────────────────────────────────────────────────────┘
```

## Files Created

### Core Modules

| File | Purpose |
|------|---------|
| `app/channels/__init__.py` | Package init, exports gateway/registry/session_sync |
| `app/channels/gateway.py` | **MultiChannelGateway** — central routing hub |
| `app/channels/registry.py` | **ChannelRegistry** — adapter management, worker-channel tracking |
| `app/channels/session_sync.py` | **SessionSync** — SQLite-backed cross-channel session state |

### Channel Adapters

| File | Purpose |
|------|---------|
| `app/channels/adapters/__init__.py` | Adapters package init |
| `app/channels/adapters/base.py` | BaseChannelAdapter, UnifiedMessage, ChannelResponse |
| `app/channels/adapters/app_adapter.py` | Msaidizi app (voice + text) |
| `app/channels/adapters/whatsapp_adapter.py` | WhatsApp via OpenWA (wraps existing bot) |
| `app/channels/adapters/sms_adapter.py` | SMS/USSD (placeholder for Africa's Talking) |
| `app/channels/adapters/voice_adapter.py` | Voice calls (placeholder for Twilio/SIP) |

### API Integration

| File | Purpose |
|------|---------|
| `app/api/v1/gateway.py` | FastAPI routes for multi-channel gateway |

### Tests

| File | Purpose |
|------|---------|
| `tests/test_multichannel_gateway.py` | Unit + integration tests |

## Key Design Decisions

### 1. Sessions Keyed by Worker, Not Channel

```python
# SAME session regardless of channel
session1 = session_sync.get_or_create_session("worker-1", ChannelType.APP_TEXT)
session2 = session_sync.get_or_create_session("worker-1", ChannelType.WHATSAPP)
assert session1.session_id == session2.session_id  # ✓ Same session!
```

This is the core insight from OpenClaw. The session belongs to the WORKER, not the CHANNEL.

### 2. Channel Adapters Normalize to UnifiedMessage

Each channel adapter converts its raw data into a `UnifiedMessage`. The gateway NEVER touches raw WhatsApp JIDs, SMS numbers, or voice DTMF codes. It only sees unified messages.

### 3. Existing WhatsApp Code Preserved

The WhatsApp adapter wraps the existing `whatsapp_bot.py` and `whatsapp_connection.py`. The gateway sits ON TOP, not replacing them. The existing `/api/v1/webhooks/whatsapp` endpoints continue to work.

### 4. SQLite for Session Storage (Hermes Pattern)

Sessions are stored in SQLite — zero-dependency, embedded, runs on Android. This follows the Hermes L1/L2 pattern. The same session store can run on-device (offline) or on the backend server.

### 5. Channel Switch Detection

The gateway detects when a worker switches channels and logs it. This is valuable for analytics (how do workers use different channels?) and for the agent (acknowledge the switch naturally).

## How to Wire Into Existing Systems

### WhatsApp (existing → gateway)

The new `/api/v1/gateway/whatsapp` endpoint replaces direct `WhatsAppBot` handling. It:
1. Verifies HMAC signature (reuses existing verification)
2. Routes through the multi-channel gateway
3. Sends response back via OpenWA

### App (existing → gateway)

The app's text/voice messages should POST to `/api/v1/gateway/message`:
```python
POST /api/v1/gateway/message
{
    "channel": "app_text",  # or "app_voice"
    "worker_id": "uuid",
    "content": "Ripoti ya leo",
    "language": "sw"
}
```

### SMS/USSD (future)

When Africa's Talking or similar is integrated:
```python
POST /api/v1/gateway/message
{
    "channel": "sms",
    "worker_id": "resolved-from-phone",
    "content": "Salio"
}
```

### Voice Calls (future)

When Twilio Voice/SIP is integrated:
```python
POST /api/v1/gateway/message
{
    "channel": "voice_call",
    "worker_id": "resolved-from-phone",
    "content": "ASR transcript of worker's speech"
}
```

## Academic Alignment

| Pattern | Unit | Alignment |
|---------|------|-----------|
| Multi-channel gateway | STA | Hub-and-spoke architecture, service mesh pattern |
| Cross-channel sessions | STA | Session management in distributed systems |
| SQLite session store | STA | Embedded database, tiered storage |
| Channel switch cost reduction | ECO 101 | Transaction cost theory — reducing friction when workers change channels |
| Unified agent across channels | ECO | Single point of value delivery, not fragmented services |

## What's Next

1. **Wire gateway into main app startup** — register adapters on app boot
2. **Integrate with existing auth flow** — ensure worker_id resolution works across channels
3. **Add Africa's Talking adapter** — real SMS/USSD integration
4. **Add Twilio Voice adapter** — real voice call integration
5. **Add proactive messaging** — gateway can push alerts to workers' preferred channel
6. **Analytics** — track channel usage patterns, channel switch frequency
7. **Offline sync** — queue messages when offline, sync when connected

## Summary

**One CFO, multiple channels, same memory.** 📱

The multi-channel gateway implements the OpenClaw pattern: a single agent system serves workers across App, WhatsApp, SMS, and Voice — with shared sessions, preserved context, and continuous conversation across channel switches. A worker starts on the app, loses network, switches to WhatsApp, and their AI CFO picks up exactly where they left off.
