# ==============================================================================
# File: src/omnicare/tentacles/followups.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Omnichannel follow-up care and device check tentacle.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Registered FollowupsTentacle & added SOP header.
# ==============================================================================

import logging
from typing import Any, Dict

from omnicare.tentacles.base import Tentacle
from omnicare.tentacles.registry import register_tentacle

logger = logging.getLogger(__name__)


@register_tentacle
class FollowupsTentacle(Tentacle):
    name = "followups"

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        text = message.get("text", "").lower()
        logger.info("Follow-up tentacle received: %s", text)
        return {
            "tentacle": self.name,
            "agent": "CareAgent",
            "response": (
                "I can help with follow-up care and scheduled device checks. "
                "If you'd like to schedule a follow-up appointment, just say: "
                "'schedule appointment'."
            ),
        }


def handle_followup(message: Dict[str, Any]) -> Dict[str, Any]:
    return FollowupsTentacle().run(message)
