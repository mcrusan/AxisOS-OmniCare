# ==============================================================================
# File: src/omnicare/config.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Centralized runtime configuration for AWS CDS channels, Amazon
#              Bedrock AgentCore, DynamoDB state persistence, and the AxisOS
#              Sovereign Triad edge nodes.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented ground-truth configuration loader.
# ==============================================================================

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_AGENTCORE_YAML = str(Path(__file__).resolve().parent / "agent" / "agentcore.yaml")


@dataclass(frozen=True)
class OmniCareConfig:
    """Immutable configuration snapshot for OmniCare runtime."""

    app_env: str = os.getenv("APP_ENV", "development")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()

    # AWS & CDS
    aws_region: str = os.getenv("AWS_REGION", "us-west-2")
    sms_origination: str = os.getenv("CDS_SMS_ORIGINATION_NUMBER", "+18005550199")
    whatsapp_phone_id: str = os.getenv("CDS_WHATSAPP_PHONE_NUMBER_ID", "waba-phone-id-001")
    ses_from_email: str = os.getenv("CDS_SES_FROM_EMAIL", "omnicare@axisos.pro")
    dynamodb_table: str = os.getenv("DYNAMODB_STATE_TABLE", "omnicare-conversation-state")

    # Bedrock AgentCore
    agentcore_config_path: str = os.getenv("AGENTCORE_CONFIG_PATH", DEFAULT_AGENTCORE_YAML)
    agentcore_model_id: str = os.getenv(
        "AGENTCORE_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
    )

    # AxisOS Sovereign Triad Edge Nodes
    zero_core_url: str = os.getenv("AXISOS_ZERO_CORE_URL", "http://192.168.1.34:8081")
    lite_url: str = os.getenv("AXISOS_LITE_URL", "http://192.168.1.34:8080")
    axis_agent_url: str = os.getenv("AXISOS_AGENT_URL", "http://192.168.1.34:8082")
    zero_comms_url: str = os.getenv("AXISOS_COMMS_URL", "http://192.168.1.34:8085")
    cloud_outpost_url: str = os.getenv(
        "AXISOS_CLOUD_OUTPOST_URL",
        "https://axisos-sovereign-triad-4zye7tn3qq-uw.a.run.app",
    )


def get_config() -> OmniCareConfig:
    return OmniCareConfig()
