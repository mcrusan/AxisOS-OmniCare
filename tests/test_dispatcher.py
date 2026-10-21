# ==============================================================================
# File: tests/test_dispatcher.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unit tests for omnichannel normalization, persistent
#              conversation_id continuity, and tentacle routing.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented cross-channel continuity tests.
# ==============================================================================

from omnicare.dispatcher.dispatcher import handle_inbound_message
from omnicare.dispatcher.state import clear_state_store, get_or_create_state


def test_cross_channel_conversation_continuity():
    clear_state_store()
    user_id = "+15035550199"

    r1 = handle_inbound_message(
        "sms",
        {
            "user_id": user_id,
            "message_id": "m1",
            "phone_number": user_id,
            "text": "Check my device status.",
            "timestamp": "2026-10-20T19:00:00Z",
        },
    )
    r2 = handle_inbound_message(
        "whatsapp",
        {
            "user_id": user_id,
            "message_id": "m2",
            "wa_id": user_id,
            "text": "Send me the full diagnostic report.",
            "timestamp": "2026-10-20T19:01:00Z",
        },
    )
    r3 = handle_inbound_message(
        "email",
        {
            "user_id": user_id,
            "message_id": "m3",
            "from_address": "operator@axisos.pro",
            "subject": "Re: Report",
            "body": "Schedule a follow-up check.",
            "timestamp": "2026-10-20T19:02:00Z",
        },
    )

    assert r1["conversation_id"] == r2["conversation_id"] == r3["conversation_id"]
    state = get_or_create_state(user_id, "sms")
    assert len(state["history"]) == 3
    assert set(state["channels_seen"]) >= {"sms", "whatsapp", "email"}


def test_tentacle_routing_appointments_and_medication():
    appt = handle_inbound_message(
        "sms",
        {
            "message_id": "m4",
            "phone_number": "+15035550199",
            "text": "I need to schedule an appointment.",
            "timestamp": "2026-10-20T19:03:00Z",
        },
    )
    assert appt["tentacle"] == "appointments"

    med = handle_inbound_message(
        "whatsapp",
        {
            "message_id": "m5",
            "wa_id": "+15035550199",
            "text": "Can I refill my medication?",
            "timestamp": "2026-10-20T19:04:00Z",
        },
    )
    assert med["tentacle"] == "medication"
