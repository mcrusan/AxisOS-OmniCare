# ==============================================================================
# File: src/omnicare/agent/__init__.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Bedrock AgentCore loader and invocation exports.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Exported load_agentcore_config, init_agentcore, run_agentcore.
# ==============================================================================

from omnicare.agent.loader import (
    init_agentcore,
    load_agentcore_config,
    run_agentcore,
)

__all__ = ["load_agentcore_config", "init_agentcore", "run_agentcore"]
