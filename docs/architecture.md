<!--
==============================================================================
File: architecture_diagram.md
Project: AxisOS OmniCare (Crusan & Co.)
Author: Marc F. Crusan / Crusan & Co. w/ AGY
Date: 2026-10-20
Description: High-contrast ASCII architecture diagram for AxisOS OmniCare.
Changelog:
  - 2026-10-20 (MFC/AGY): Updated with real AxisOS Sovereign Triad ports & services.
==============================================================================
-->

```text
                   ┌────────────────────────────────────────────────────┐
                   │             AWS CDS Omnichannel Ingress            │
                   │  SMS • RCS • WhatsApp (End User Messaging) • SES   │
                   └─────────────────────────┬──────────────────────────┘
                                             │
                                             ▼
                   ┌────────────────────────────────────────────────────┐
                   │        OmniCare Conversation Router (FastAPI)      │
                   │  • Normalizes SMS / RCS / WhatsApp / Email         │
                   │  • Resolves deterministic cross-channel conv_id    │
                   │  • Synchronizes state with Amazon DynamoDB         │
                   └─────────────────────────┬──────────────────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
     ┌───────────────────────────────────┐       ┌───────────────────────────────────┐
     │   Amazon Bedrock AgentCore        │       │   Deterministic Action Tentacles  │
     │ • CareAgent     • AxisAgent       │◄─────►│ • AxisOSBridgeTentacle (/proc)    │
     │ • SummaryAgent  • SupportAgent    │       │ • ChannelSwitch (WA/SMS -> SES)   │
     │ • SetupAgent                      │       │ • Followups / Appointments / Meds │
     └─────────────────┬─────────────────┘       └─────────────────┬─────────────────┘
                       │                                           │
                       └─────────────────────┬─────────────────────┘
                                             ▼
                   ┌────────────────────────────────────────────────────┐
                   │          AxisOS Sovereign Triad Edge Layer         │
                   │ • zero-core (:8081)  — 49 KB C99 RAMDisk Mind      │
                   │ • agent-lite (:8080) — Tactical Router & Vanguard  │
                   │ • axis-agent (:8082) — Supervisor & Tentacles      │
                   │ • zero-comms (:8085) — Comms Center Web HUD        │
                   │ • Outpost Cloud-01   — Freestanding C99 Cloud Run  │
                   └────────────────────────────────────────────────────┘
```
