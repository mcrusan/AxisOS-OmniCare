# ==============================================================================
# File: src/omnicare/utils/logging.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Structured CloudWatch & local audit logging utilities.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented structured logging helper.
# ==============================================================================

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict


def configure_logging(level: str = None) -> logging.Logger:
    resolved_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    logging.basicConfig(
        level=getattr(logging, resolved_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger("omnicare")


def format_audit_event(
    event_type: str,
    conversation_id: str,
    channel: str,
    details: Dict[str, Any],
) -> str:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "vendor": "Crusan & Co.",
        "platform": "AxisOS OmniCare",
        "event_type": event_type,
        "conversation_id": conversation_id,
        "channel": channel,
        "details": details,
    }
    return json.dumps(record, sort_keys=True)
