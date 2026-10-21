# ==============================================================================
# File: src/omnicare/tentacles/echo.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Diagnostic echo tentacle for omnichannel round-trip verification.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Integrated EchoTentacle with SOP header.
# ==============================================================================

from typing import Any, Dict
from omnicare.tentacles.base import Tentacle
from omnicare.tentacles.registry import register_tentacle


@register_tentacle
class EchoTentacle(Tentacle):
    name = "echo"

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        raw = message.get("text", "")
        if raw.lower().startswith("echo "):
            payload = raw[5:].strip()
        else:
            payload = raw
        return {
            "tentacle": self.name,
            "response": f"You said: {payload}",
        }


def handle_echo(message: Dict[str, Any]) -> Dict[str, Any]:
    return EchoTentacle().run(message)
