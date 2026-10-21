# ==============================================================================
# File: tests/test_sms.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unit tests for AWS CDS SMS and RCS inbound/outbound handling.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented SMS/RCS unit tests.
# ==============================================================================

from omnicare.channels.sms import send_sms
from omnicare.dispatcher.dispatcher import handle_inbound_message


def test_send_sms_audit_mode():
    receipt = send_sms("+15035550142", "AxisOS Sovereign Triad test pulse")
    assert "MessageId" in receipt
    assert receipt["Channel"] == "sms"


def test_inbound_sms_axisos_status():
    payload = {
        "message_id": "sms-test-1",
        "phone_number": "+15035550142",
        "text": "Check my device status.",
        "timestamp": "2026-10-20T19:00:00Z",
    }
    res = handle_inbound_message("sms", payload)
    assert res["tentacle"] == "axisos"
    assert res["agent"] == "AxisAgent"
    assert "RAMGAK Zone" in res["response"]
    assert "telemetry" in res
