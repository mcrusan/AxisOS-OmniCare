# ==============================================================================
# File: server/__init__.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Top-level server package forwarding to omnicare.server.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Populated top-level server package init.
# ==============================================================================

from omnicare.server.api import router

__all__ = ["router"]
