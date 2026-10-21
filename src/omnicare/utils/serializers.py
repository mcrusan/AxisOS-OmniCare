# ==============================================================================
# File: src/omnicare/utils/serializers.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Payload normalization and canonical response serializers for
#              SMS, RCS, WhatsApp, and Amazon SES Email channels.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented canonical omnichannel serializers.
# ==============================================================================

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict


def derive_conversation_id(sender: str) -> str:
    """
    Derives a deterministic cross-channel conversation_id from a normalized
    user identifier or phone/email handle so SMS, WhatsApp, RCS, and Email
    share one continuous conversation thread.
    """
    clean = (sender or "anonymous").strip().lower()
    digest = hashlib.sha256(clean.encode("utf-8")).hexdigest()[:12]
    return f"conv-{digest}"


def serialize_cds_envelope(
    channel: str,
    sender: str,
    text: str,
    message_id: str = "",
    subject: str = "",
    timestamp: str = "",
    user_id: str = "",
) -> Dict[str, Any]:
    resolved_user = (user_id or sender or "anonymous").strip()
    conv_id = derive_conversation_id(resolved_user)
    return {
        "conversation_id": conv_id,
        "user_id": resolved_user,
        "channel": channel.lower(),
        "sender": sender,
        "subject": subject,
        "text": text or "",
        "message_id": message_id or f"msg-{conv_id}",
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
    }
