# ==============================================================================
# File: src/omnicare/tentacles/base.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Abstract base class for all OmniCare action tentacles.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Integrated base Tentacle class into repo tree.
# ==============================================================================

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class Tentacle:
    """
    Base class for all OmniCare tentacles.
    Each tentacle implements a deterministic `run()` method.
    """

    name: str = "base"

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Tentacle must implement run()")
