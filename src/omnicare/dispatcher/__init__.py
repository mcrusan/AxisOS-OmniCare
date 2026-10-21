# ==============================================================================
# File: src/omnicare/dispatcher/__init__.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Dispatcher module exports.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Exported handle_inbound_message and state helpers.
# ==============================================================================

from omnicare.dispatcher.dispatcher import (
    handle_email,
    handle_inbound_message,
    handle_sms,
    handle_whatsapp,
    normalize_message,
)
from omnicare.dispatcher.state import (
    clear_state_store,
    get_or_create_state,
    record_turn,
)

__all__ = [
    "handle_inbound_message",
    "normalize_message",
    "handle_sms",
    "handle_whatsapp",
    "handle_email",
    "get_or_create_state",
    "record_turn",
    "clear_state_store",
]
