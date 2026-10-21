# ==============================================================================
# File: server/webhook_sms.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: AWS Lambda / API Gateway handler for inbound CDS SMS & RCS events.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented Lambda-compatible SMS/RCS webhook handler.
# ==============================================================================

from typing import Any, Dict
from omnicare.dispatcher.dispatcher import handle_inbound_message


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """AWS Lambda entrypoint for AWS CDS SMS and RCS inbound webhooks."""
    channel = event.get("channel", "sms")
    return handle_inbound_message(channel, event)
