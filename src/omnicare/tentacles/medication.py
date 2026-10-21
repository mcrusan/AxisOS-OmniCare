# ==============================================================================
# File: src/omnicare/tentacles/medication.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Omnichannel medication and prescription refill tentacle.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Registered MedicationTentacle & added SOP header.
# ==============================================================================

import logging
from typing import Any, Dict

from omnicare.tentacles.base import Tentacle
from omnicare.tentacles.registry import register_tentacle

logger = logging.getLogger(__name__)


@register_tentacle
class MedicationTentacle(Tentacle):
    name = "medication"

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        text = message.get("text", "").lower()
        logger.info("Medication tentacle received: %s", text)
        return {
            "tentacle": self.name,
            "agent": "CareAgent",
            "response": (
                "I can help with medication questions or refills. "
                "To request a refill, say: 'refill my prescription'."
            ),
        }


def handle_medication(message: Dict[str, Any]) -> Dict[str, Any]:
    return MedicationTentacle().run(message)
