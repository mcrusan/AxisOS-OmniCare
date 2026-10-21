# ==============================================================================
# File: server/api.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Top-level webhook router wrapper forwarding to omnicare.server.api.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Populated top-level server/api.py.
# ==============================================================================

from omnicare.server.api import (
    InboundEmail,
    InboundSMS,
    InboundWhatsApp,
    email_webhook,
    rcs_webhook,
    router,
    sms_webhook,
    whatsapp_webhook,
)

__all__ = [
    "router",
    "InboundSMS",
    "InboundWhatsApp",
    "InboundEmail",
    "sms_webhook",
    "rcs_webhook",
    "whatsapp_webhook",
    "email_webhook",
]
