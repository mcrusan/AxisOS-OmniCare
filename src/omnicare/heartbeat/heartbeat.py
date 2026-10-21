# ==============================================================================
# File: src/omnicare/heartbeat/heartbeat.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Sovereign Triad & Node 001 ([💃🍪🕺]) heartbeat monitor for
#              cloud-to-edge observability.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented Sovereign Triad heartbeat pulse collector.
# ==============================================================================

from datetime import datetime, timezone
from typing import Any, Dict

from omnicare.config import get_config
from omnicare.tentacles.axisos_bridge import (
    probe_triad_endpoint,
    read_live_machine_telemetry,
)


def collect_triad_heartbeat(probe_network: bool = False) -> Dict[str, Any]:
    """
    Returns a structured heartbeat snapshot combining local /proc and /sys
    ground-truth telemetry with AxisOS Sovereign Triad node descriptors.
    """
    cfg = get_config()
    telemetry = read_live_machine_telemetry()

    nodes = {
        "zero_core": {"url": cfg.zero_core_url, "port": 8081, "role": "C99 RAMDisk Mind"},
        "agent_lite": {"url": cfg.lite_url, "port": 8080, "role": "Tactical Router & Vanguard"},
        "axis_agent": {"url": cfg.axis_agent_url, "port": 8082, "role": "Supervisor & Tentacles"},
        "zero_comms": {"url": cfg.zero_comms_url, "port": 8085, "role": "Comms Center Web HUD"},
        "cloud_outpost_01": {
            "url": cfg.cloud_outpost_url,
            "port": 443,
            "role": "Freestanding C99 Cloud Run Outpost",
        },
    }

    if probe_network:
        for key, meta in nodes.items():
            meta["probe"] = probe_triad_endpoint(meta["url"])

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "signature": "[💃🍪🕺]",
        "status": "ONLINE",
        "ramgak_zone": telemetry.get("ramgak_zone", "GREEN"),
        "telemetry": telemetry,
        "triad_nodes": nodes,
    }
