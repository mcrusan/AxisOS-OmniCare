<!--
==============================================================================
File: README.md
Project: AxisOS OmniCare (Crusan & Co.)
Author: Marc F. Crusan / Crusan & Co. w/ AGY
Date: 2026-10-20
Description: Production GitHub README for AxisOS OmniCare — Unified AWS
             Communication Developer Services (CDS) + Amazon Bedrock AgentCore
             + AxisOS Sovereign Triad Cloud-to-Edge Control Plane.
Changelog:
  - 2026-10-20 (MFC/AGY): Replaced 0-byte placeholder with full technical README.
==============================================================================
-->

# Crusan & Co. — AxisOS OmniCare
### **Unified Agentic Conversations Across AWS CDS + Real-World Edge Execution via AxisOS**

**Parent Entity:** Crusan & Co.  
**Flagship Platform:** AxisOS (`HONEST` • `AUDITABLE` • `OWNED`)  
**Architect:** Marc F. Crusan (w/ AGY)  
**Hackathon Track:** AWS Communication Developer Services (CDS) & Amazon Bedrock AgentCore  
**2m15s 1080p Video Walkthrough:** [https://youtu.be/WyP8PuIEWjs](https://youtu.be/WyP8PuIEWjs)  

> **Intellectual Property & Proprietary Core Exclusion Notice:** This repository contains the external **AxisOS OmniCare** AWS CDS / Amazon Bedrock AgentCore integration layer and HTTP telemetry bridge (`axisos_bridge.py`). The underlying **AxisOS Tiny OS** (`axisos-initramfs.img`), the **freestanding C99 direct kernel syscall stack** (`axis-syscalls.c`, `axis-loop.c`, `svc #0` / `syscall`), the **AxisOS Sovereign Triad core agents** (`zero-core`, `agent-lite` / `lite`, `axis-agent`, `zero-comms`, `zero-brain`, and `cloud-triad-gateway`), the `RAMGAK` DDR4 memory bracket architecture, and all pre-loaded AxisOS hardware distributions are not distributed in this repository and remain the exclusive, proprietary intellectual property of **Crusan & Co.** (Marc F. Crusan). All Rights Reserved.

---

## 1. Executive Summary

**AxisOS OmniCare** is an agentic, omnichannel conversation and edge-control system built on **AWS Communication Developer Services (CDS / AWS End User Messaging)** and **Amazon Simple Email Service (SES)**. It unifies **SMS, RCS, WhatsApp, and Email** into a single continuous conversation thread (`conversation_id`), orchestrated by **Amazon Bedrock AgentCore**, and extends cloud intelligence directly into physical hardware through the **AxisOS Sovereign Triad** running in `RAMGAK`-bracketed DDR4 RAM on Raspberry Pi edge nodes.

Unlike conventional chatbots that lose context when a user moves from SMS to WhatsApp or Email—and cannot perform deterministic actions in the physical world—OmniCare acts as a **Cloud-to-Edge Conversational Control Plane**:

- **One Persistent `conversation_id` Across All 4 Channels**: Seamless state continuity across AWS CDS **SMS**, **RCS**, **WhatsApp** (with approved Meta Utility Templates), and **Amazon SES Inbound/Outbound Email**.
- **Intent-Driven Channel Switching (`SummaryAgent`)**: Automatically escalates mobile SMS/WhatsApp inquiries into rich, long-form **Amazon SES diagnostic reports** when the payload exceeds mobile chat ergonomics, while confirming delivery on the originating channel.
- **Multi-Agent Orchestration (`Amazon Bedrock AgentCore`)**: Coordinates 5 specialized agents (`CareAgent`, `AxisAgent`, `SummaryAgent`, `SupportAgent`, `SetupAgent`) and 8 deterministic Action Group tools.
- **Real-World Edge Execution (`AxisOS Sovereign Triad`)**: Dispatches verified commands and reads ground-truth kernel telemetry (`/proc/loadavg`, `/proc/meminfo`, `/sys/class/thermal`, `/proc/net/dev`) from freestanding C99 edge services (`zero-core :8081` at `~112 µs` latency, `lite :8080`, `axis-agent :8082`, `zero-comms :8085`).

---

## 2. System Architecture

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

---

## 3. Repository Structure

```text
omnicare/
├── Dockerfile                          # Production container build
├── LICENSE                             # Crusan & Co. MIT License
├── README.md                           # Architecture & deployment guide
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variable template
├── infra/
│   ├── aws_cds_config.json             # AWS CDS SMS, RCS, WhatsApp templates & SES config
│   ├── bedrock_config.json             # Amazon Bedrock AgentCore multi-agent schema
│   └── docker-compose.yml              # Container orchestration stack
├── scripts/
│   ├── demo_scenario.md                # 4-stage hackathon video walkthrough
│   └── seed_test_messages.py           # Runnable 4-stage omnichannel verification script
├── server/
│   ├── api.py                          # Top-level FastAPI webhook router export
│   ├── webhook_sms.py                  # AWS Lambda handler for CDS SMS & RCS
│   ├── webhook_whatsapp.py             # AWS Lambda handler for CDS WhatsApp
│   └── webhook_email.py                # AWS Lambda handler for Amazon SES inbound
├── src/omnicare/
│   ├── main.py                         # FastAPI application entrypoint
│   ├── config.py                       # Centralized environment & Triad endpoint loader
│   ├── agent/
│   │   ├── agentcore.yaml              # Bedrock AgentCore multi-agent & tool definitions
│   │   └── loader.py                   # Bedrock runtime client & deterministic audit fallback
│   ├── channels/
│   │   ├── sms.py                      # AWS CDS / SNS SMS & RCS outbound sender
│   │   ├── whatsapp.py                 # AWS End User Messaging Social (WhatsApp + Meta Templates)
│   │   └── email.py                    # Amazon SES outbound report dispatcher
│   ├── dispatcher/
│   │   ├── dispatcher.py               # Cross-channel normalization & intent router
│   │   └── state.py                    # Persistent conversation_id continuity store
│   ├── heartbeat/
│   │   └── heartbeat.py                # Sovereign Triad & [💃🍪🕺] pulse collector
│   ├── server/
│   │   └── api.py                      # FastAPI /webhook/* and /axisos/* routes
│   ├── tentacles/
│   │   ├── base.py                     # Base Tentacle interface
│   │   ├── registry.py                 # Decorator-driven tentacle registry
│   │   ├── axisos_bridge.py            # Live /proc & /sys telemetry + edge task execution
│   │   ├── appointments.py             # Care appointment scheduling tentacle
│   │   ├── followups.py                # Care & device follow-up tentacle
│   │   ├── medication.py               # Prescription & medication continuity tentacle
│   │   ├── echo.py                     # Diagnostic round-trip echo tentacle
│   │   └── help.py                     # Interactive omnichannel command menu
│   └── utils/
│       ├── logging.py                  # Structured CloudWatch & JSONL audit logger
│       ├── serializers.py              # Deterministic conversation_id & envelope serializers
│       └── validation.py               # E.164, email, and AxisOS action allowlist validators
└── tests/
    ├── test_sms.py                     # SMS & RCS channel unit tests
    ├── test_whatsapp.py                # WhatsApp Meta Template & channel switch tests
    ├── test_email.py                   # Amazon SES inbound/outbound unit tests
    ├── test_dispatcher.py              # Cross-channel conversation_id continuity tests
    └── test_agentcore.py               # Bedrock AgentCore config & inference tests
```

---

## 4. Quick Start & Verification

### Run the 4-Stage Omnichannel Demo Simulation
```bash
PYTHONPATH=src python3 scripts/seed_test_messages.py
```
This executes all four stages of the demo flow under a single persistent `conversation_id`:
1. **SMS -> AxisOS Telemetry**: Queries live `/proc` and `/sys` hardware state (`RAMGAK` memory bracket, load average, SoC temperature `°C`, and active NIC packet counters).
2. **WhatsApp -> Amazon SES Email Switch**: `SummaryAgent` detects a request for a full diagnostic report, switches channels to **Amazon SES**, emails the full report, and confirms the switch on WhatsApp.
3. **SES Email Reply -> Follow-Up Workflow**: Continues the exact same conversation thread from an inbound email reply to schedule a follow-up check.
4. **SMS -> Real-World Edge Action**: Validates and executes an AxisOS edge checkpoint/restart check.

### Run the Unit Test Suite
```bash
PYTHONPATH=src pytest -v
```

### Start the Live FastAPI Server
```bash
PYTHONPATH=src uvicorn omnicare.main:app --host 0.0.0.0 --port 8000
```

---

## 5. Built by Crusan & Co.
- **2m15s Hackathon Demo Video (YouTube):** [https://youtu.be/WyP8PuIEWjs](https://youtu.be/WyP8PuIEWjs)
- **Website & Live Sovereign Fleet Deck:** [https://axisos.pro](https://axisos.pro)
- **Three Pillars of AxisOS:** `HONEST` (Ground-truth telemetry, zero mock data) • `AUDITABLE` (Inspectable at every layer) • `OWNED` (Sovereign hardware control)
