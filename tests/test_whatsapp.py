# ==============================================================================
# File: tests/test_whatsapp.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unit tests for AWS End User Messaging Social (WhatsApp) text
#              and Meta Template dispatch plus channel switching.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented WhatsApp and Meta Template unit tests.
# ==============================================================================

from omnicare.channels.whatsapp import send_whatsapp
from omnicare.dispatcher.dispatcher import handle_inbound_message


def test_send_whatsapp_template():
    receipt = send_whatsapp(
        "+15035550142",
        "Fallback body",
        template_name="axisos_telemetry_alert",
        template_params=["pp-core-pri", "41.2", "GREEN", "112"],
    )
    assert "messageId" in receipt
    assert receipt["template"] == "axisos_telemetry_alert"
    assert receipt["meta_payload"]["type"] == "template"


def test_whatsapp_to_email_channel_switch():
    payload = {
        "message_id": "wa-test-1",
        "wa_id": "+15035550142",
        "text": "Send me the full diagnostic report.",
        "email": "operator@axisos.pro",
        "timestamp": "2026-10-20T19:00:00Z",
    }
    res = handle_inbound_message("whatsapp", payload)
    assert res["tentacle"] == "channel_switch"
    assert res["agent"] == "SummaryAgent"
    assert res["switched_from"] == "whatsapp"
    assert res["switched_to"] == "email"
    assert "MessageId" in res["ses_dispatch"]
