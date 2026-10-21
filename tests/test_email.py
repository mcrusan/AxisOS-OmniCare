# ==============================================================================
# File: tests/test_email.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unit tests for Amazon SES outbound and inbound email workflows.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented SES email unit tests.
# ==============================================================================

from omnicare.channels.email import send_email
from omnicare.dispatcher.dispatcher import handle_inbound_message


def test_send_email_audit_mode():
    receipt = send_email(
        "operator@axisos.pro",
        "AxisOS Diagnostic Report",
        "Sovereign Triad telemetry verified.",
    )
    assert "MessageId" in receipt
    assert receipt["Channel"] == "email"
    assert receipt["To"] == "operator@axisos.pro"


def test_inbound_email_followup_workflow():
    payload = {
        "message_id": "ses-test-1",
        "from_address": "operator@axisos.pro",
        "subject": "Re: AxisOS Diagnostic Report",
        "body": "Schedule a follow-up check.",
        "timestamp": "2026-10-20T19:00:00Z",
    }
    res = handle_inbound_message("email", payload)
    assert res["tentacle"] == "followups"
    assert "follow-up" in res["response"].lower()
