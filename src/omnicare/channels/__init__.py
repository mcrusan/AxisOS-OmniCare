# ==============================================================================
# File: src/omnicare/channels/__init__.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Omnichannel outbound dispatch exports (SMS, RCS, WhatsApp, Email).
# Changelog:
#   - 2026-10-20 (MFC/AGY): Exported send_sms, send_whatsapp, and send_email.
# ==============================================================================

from omnicare.channels.email import send_email
from omnicare.channels.sms import send_sms
from omnicare.channels.whatsapp import send_whatsapp

__all__ = ["send_sms", "send_whatsapp", "send_email"]
