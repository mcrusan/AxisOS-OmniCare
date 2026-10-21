# ==============================================================================
# File: src/omnicare/tentacles/__init__.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Exports all OmniCare action tentacles and registry helpers.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Registered appointments, followups, medication,
#     echo, help, and axisos tentacles.
# ==============================================================================

from omnicare.tentacles.appointments import AppointmentsTentacle, handle_appointment
from omnicare.tentacles.axisos_bridge import (
    AxisOSBridgeTentacle,
    handle_axisos,
    read_live_machine_telemetry,
)
from omnicare.tentacles.base import Tentacle
from omnicare.tentacles.echo import EchoTentacle, handle_echo
from omnicare.tentacles.followups import FollowupsTentacle, handle_followup
from omnicare.tentacles.help import HelpTentacle, handle_help
from omnicare.tentacles.medication import MedicationTentacle, handle_medication
from omnicare.tentacles.registry import (
    TENTACLE_REGISTRY,
    get_tentacle,
    list_tentacles,
    register_tentacle,
)

__all__ = [
    "Tentacle",
    "TENTACLE_REGISTRY",
    "register_tentacle",
    "get_tentacle",
    "list_tentacles",
    "AppointmentsTentacle",
    "FollowupsTentacle",
    "MedicationTentacle",
    "EchoTentacle",
    "HelpTentacle",
    "AxisOSBridgeTentacle",
    "handle_appointment",
    "handle_followup",
    "handle_medication",
    "handle_echo",
    "handle_help",
    "handle_axisos",
    "read_live_machine_telemetry",
]
