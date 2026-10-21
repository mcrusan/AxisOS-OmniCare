# ==============================================================================
# File: src/omnicare/tentacles/help.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Interactive help menu tentacle across SMS, RCS, WhatsApp, Email.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Expanded help menu with AxisOS Sovereign Triad commands.
# ==============================================================================

from typing import Any, Dict
from omnicare.tentacles.base import Tentacle
from omnicare.tentacles.registry import register_tentacle


@register_tentacle
class HelpTentacle(Tentacle):
    name = "help"

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tentacle": self.name,
            "response": (
                "Crusan & Co. — AxisOS OmniCare Command Menu:\n"
                "- 'status' or 'check device' -> Live AxisOS Sovereign Triad & RAMGAK telemetry\n"
                "- 'full diagnostic report' -> Switch channel & dispatch full report via Amazon SES Email\n"
                "- 'restart device' or 'checkpoint' -> Execute verified AxisOS Edge action\n"
                "- 'schedule followup' -> Book follow-up check in continuity ledger\n"
                "- 'schedule appointment' -> Coordinate care/field appointment\n"
                "- 'refill medication' -> Medication & prescription continuity\n"
                "- 'echo <text>' -> Diagnostic round-trip echo"
            ),
        }


def handle_help(message: Dict[str, Any]) -> Dict[str, Any]:
    return HelpTentacle().run(message)
