# ==============================================================================
# File: server/webhook_whatsapp.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: AWS Lambda / API Gateway handler for inbound CDS WhatsApp events.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented Lambda-compatible WhatsApp webhook handler.
# ==============================================================================

from typing import Any, Dict
from omnicare.dispatcher.dispatcher import handle_inbound_message


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """AWS Lambda entrypoint for AWS End User Messaging Social (WhatsApp) inbound webhooks."""
    return handle_inbound_message("whatsapp", event)
