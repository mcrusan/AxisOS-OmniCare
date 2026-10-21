# ==============================================================================
# File: src/omnicare/server/__init__.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Server webhook router exports.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Exported FastAPI webhook router.
# ==============================================================================

from omnicare.server.api import router

__all__ = ["router"]
