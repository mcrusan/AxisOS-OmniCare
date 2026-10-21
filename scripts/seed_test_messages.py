#!/usr/bin/env python3
# ==============================================================================
# File: scripts/seed_test_messages.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: End-to-end 4-stage omnichannel simulation script exercising
#              SMS, WhatsApp, Amazon SES Email channel switching, and live
#              AxisOS Sovereign Triad edge telemetry under one conversation_id.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented runnable 4-stage demo verification script.
# ==============================================================================

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from omnicare.dispatcher.dispatcher import handle_inbound_message
from omnicare.dispatcher.state import get_or_create_state


def main() -> int:
    operator_id = "+15035550142"
    print("======================================================================")
    print(" Crusan & Co. — AxisOS OmniCare 4-Stage Omnichannel Demo Verification")
    print("======================================================================\n")

    # Stage 1: SMS -> AxisOS Status
    stage1_payload = {
        "user_id": operator_id,
        "message_id": "sms-001",
        "phone_number": operator_id,
        "text": "Check my device status.",
        "timestamp": "2026-10-20T19:00:00Z",
    }
    res1 = handle_inbound_message("sms", stage1_payload)
    print("[STAGE 1: SMS -> AxisOS Sovereign Triad Status]")
    print(json.dumps(res1, indent=2))
    print()

    # Stage 2: WhatsApp -> Email Channel Switch
    stage2_payload = {
        "user_id": operator_id,
        "message_id": "wa-002",
        "wa_id": operator_id,
        "text": "Send me the full diagnostic report.",
        "email": "operator@axisos.pro",
        "timestamp": "2026-10-20T19:00:45Z",
    }
    res2 = handle_inbound_message("whatsapp", stage2_payload)
    print("[STAGE 2: WhatsApp -> SummaryAgent Channel Switch to Amazon SES Email]")
    print(json.dumps(res2, indent=2))
    print()

    # Stage 3: Email -> Follow-Up Workflow
    stage3_payload = {
        "user_id": operator_id,
        "message_id": "ses-003",
        "from_address": "operator@axisos.pro",
        "subject": "Re: AxisOS Sovereign Triad Diagnostic Report",
        "body": "Schedule a follow-up check.",
        "timestamp": "2026-10-20T19:01:30Z",
    }
    res3 = handle_inbound_message("email", stage3_payload)
    print("[STAGE 3: Amazon SES Inbound Email -> CareAgent Follow-Up Workflow]")
    print(json.dumps(res3, indent=2))
    print()

    # Stage 4: SMS -> Real-World AxisOS Edge Action
    stage4_payload = {
        "user_id": operator_id,
        "message_id": "sms-004",
        "phone_number": operator_id,
        "text": "Restart the device and checkpoint.",
        "timestamp": "2026-10-20T19:02:15Z",
    }
    res4 = handle_inbound_message("sms", stage4_payload)
    print("[STAGE 4: SMS -> AxisOS Edge Action Execution]")
    print(json.dumps(res4, indent=2))
    print()

    # Inspect unified state across all 4 turns
    unified_state = get_or_create_state(operator_id, "sms")
    print("[UNIFIED CONVERSATION CONTINUITY STATE]")
    print(
        json.dumps(
            {
                "conversation_id": unified_state["conversation_id"],
                "user_id": unified_state["user_id"],
                "channels_seen": unified_state["channels_seen"],
                "preferred_channel": unified_state["preferred_channel"],
                "turns_recorded": len(unified_state["history"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
