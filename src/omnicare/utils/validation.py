# ==============================================================================
# File: src/omnicare/utils/validation.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Input validation for E.164 phone numbers, WhatsApp IDs, email
#              addresses, and AxisOS Sovereign Triad commands.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Added channel and edge command validators.
# ==============================================================================

import re
from typing import Tuple

E164_REGEX = re.compile(r"^\+?[1-9]\d{6,14}$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

ALLOWED_AXISOS_ACTIONS = {
    "status",
    "telemetry",
    "triad",
    "ping",
    "checkpoint",
    "sync",
    "restart_comms",
    "reboot_check",
}


def validate_phone_or_wa(identifier: str) -> bool:
    if not identifier:
        return False
    cleaned = re.sub(r"[\s\-\(\)]", "", identifier)
    return bool(E164_REGEX.match(cleaned))


def validate_email(address: str) -> bool:
    if not address:
        return False
    return bool(EMAIL_REGEX.match(address.strip()))


def validate_axisos_action(action: str) -> Tuple[bool, str]:
    normalized = (action or "").strip().lower()
    if normalized in ALLOWED_AXISOS_ACTIONS:
        return True, normalized
    return False, f"Action '{action}' is not in the auditable AxisOS allowlist."
