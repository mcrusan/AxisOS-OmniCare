# ==============================================================================
# File: server/webhook_email.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: AWS Lambda / Amazon SES Inbound Receipt Rule handler.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented Lambda-compatible SES email webhook handler.
# ==============================================================================

from typing import Any, Dict
from omnicare.dispatcher.dispatcher import handle_inbound_message


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """AWS Lambda entrypoint for Amazon SES inbound email events."""
    return handle_inbound_message("email", event)
