# ==============================================================================
# File: tests/test_agentcore.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unit tests for Amazon Bedrock AgentCore YAML loader and
#              deterministic inference fallback.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented AgentCore config and invocation tests.
# ==============================================================================

from omnicare.agent.loader import load_agentcore_config, run_agentcore


def test_load_agentcore_config():
    cfg = load_agentcore_config()
    assert cfg["vendor"] == "Crusan & Co."
    assert cfg["project"] == "AxisOS OmniCare"
    assert "CareAgent" in cfg["agents"]
    assert "AxisAgent" in cfg["agents"]
    assert "SummaryAgent" in cfg["agents"]


def test_run_agentcore_deterministic():
    res = run_agentcore("Summarize node connectivity across the shop mesh.", agent_name="AxisAgent")
    assert res["agent"] == "AxisAgent"
    assert "agentcore_response" in res
