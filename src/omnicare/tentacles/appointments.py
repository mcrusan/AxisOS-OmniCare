# ==============================================================================
# File: src/omnicare/tentacles/appointments.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Omnichannel appointment scheduling tentacle registered with
#              the OmniCare tentacle registry.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Registered AppointmentsTentacle & added SOP header.
# ==============================================================================

import logging
from typing import Any, Dict

from omnicare.tentacles.base import Tentacle
from omnicare.tentacles.registry import register_tentacle

logger = logging.getLogger(__name__)


@register_tentacle
class AppointmentsTentacle(Tentacle):
    name = "appointments"

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        text = message.get("text", "").lower()
        logger.info("Appointment tentacle received: %s", text)
        return {
            "tentacle": self.name,
            "agent": "CareAgent",
            "response": (
                "To schedule an appointment, please provide a preferred date and time. "
                "For example: 'appointment next Tuesday at 3pm'."
            ),
        }


def handle_appointment(message: Dict[str, Any]) -> Dict[str, Any]:
    return AppointmentsTentacle().run(message)
