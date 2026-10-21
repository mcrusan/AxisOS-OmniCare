<!--
==============================================================================
File: scripts/demo_scenario.md
Project: AxisOS OmniCare (Crusan & Co.)
Author: Marc F. Crusan / Crusan & Co. w/ AGY
Date: 2026-10-20
Description: Step-by-step runnable demo scenario for the 3-minute AWS CDS
             Hackathon video and live verification.
Changelog:
  - 2026-10-20 (MFC/AGY): Documented 4-stage omnichannel cloud-to-edge demo.
==============================================================================
-->

# Crusan & Co. — AxisOS OmniCare 4-Stage Demo Scenario

Run the automated end-to-end simulation at any time:

```bash
PYTHONPATH=src python3 scripts/seed_test_messages.py
```

---

## Stage 1: Inbound SMS -> AxisOS Sovereign Triad Telemetry
- **Channel**: AWS CDS SMS (`+15035550142`)
- **Inbound Message**: `"Check my device status."`
- **Orchestration**:
  1. Enters `/webhook/sms` and normalizes into `conversation_id: conv-b09df0c607b2`.
  2. Routes to `AxisAgent` (`AxisOSBridgeTentacle`), reading live `/proc/meminfo`, `/proc/loadavg`, `/sys/class/thermal/thermal_zone0/temp`, and `/proc/net/dev`.
  3. Replies via SMS with live `RAMGAK` Green Zone memory bracket, 1-minute load, SoC temperature (`°C`), and active NICs.

---

## Stage 2: Inbound WhatsApp -> Intent-Driven Switch to Amazon SES Email
- **Channel**: AWS End User Messaging Social / WhatsApp (`+15035550142`)
- **Inbound Message**: `"Send me the full diagnostic report."`
- **Orchestration**:
  1. Enters `/webhook/whatsapp` and attaches to the **exact same `conversation_id`** (`conv-b09df0c607b2`).
  2. `SummaryAgent` recognizes that a full hardware & network diagnostic report exceeds mobile chat ergonomics and invokes `SwitchChannel` -> `SendEmail` via Amazon SES (`operator@axisos.pro`).
  3. Confirms the channel switch back to the operator on WhatsApp with the SES `MessageId`.

---

## Stage 3: Inbound Email Reply -> Multi-Step Follow-Up Workflow
- **Channel**: Amazon SES Inbound Email (`operator@axisos.pro`, linked to `conv-b09df0c607b2`)
- **Inbound Message**: `"Schedule a follow-up check."`
- **Orchestration**:
  1. Enters `/webhook/email` preserving `conversation_id: conv-b09df0c607b2`.
  2. `CareAgent` (`FollowupsTentacle`) records the follow-up in the conversation state store and confirms via SMS/WhatsApp.

---

## Stage 4: Real-World Edge Action on AxisOS Hardware
- **Channel**: AWS CDS SMS (`+15035550142`)
- **Inbound Message**: `"Restart the device and run checkpoint."`
- **Orchestration**:
  1. `AxisAgent` validates the command against the auditable AxisOS action allowlist (`checkpoint` / `reboot_check`).
  2. Triggers the edge task on the AxisOS Sovereign Triad node and returns verified post-action telemetry.
