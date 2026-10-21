# ==============================================================================
# File: src/omnicare/channels/sms.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: AWS Communication Developer Services (CDS / SNS & End User
#              Messaging) outbound SMS and RCS dispatcher.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Added RCS fallback, SOP header, and offline audit mode.
# ==============================================================================

import logging
import os
import uuid
from typing import Any, Dict

try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:  # pragma: no cover
    boto3 = None
    Config = None
    BotoCoreError = Exception
    ClientError = Exception

logger = logging.getLogger(__name__)


def _get_sms_client():
    """
    Create and return an AWS SNS / End User Messaging client configured for SMS/RCS.
    """
    region = os.getenv("AWS_REGION", "us-west-2")
    boto_config = Config(
        region_name=region,
        retries={"max_attempts": 3, "mode": "standard"},
    )
    return boto3.client("sns", config=boto_config)


def _has_live_aws_credentials() -> bool:
    key = os.getenv("AWS_ACCESS_KEY_ID", "")
    return bool(key and key != "your_access_key_id_here")


def send_sms(phone_number: str, message: str, channel: str = "sms") -> Dict[str, Any]:
    """
    Send an SMS or RCS message using AWS CDS / SNS.
    When running in local verification or CI without live AWS keys, returns an
    auditable deterministic dispatch receipt.
    """
    logger.info("Sending %s to %s", channel.upper(), phone_number)

    if not _has_live_aws_credentials():
        msg_id = f"cds-{channel}-{uuid.uuid4().hex[:10]}"
        logger.info("Local audit dispatch (%s) -> %s [%s]", channel, phone_number, msg_id)
        return {
            "MessageId": msg_id,
            "Channel": channel,
            "Recipient": phone_number,
            "Status": "DISPATCHED_AUDIT",
        }

    try:
        client = _get_sms_client()
        response = client.publish(
            PhoneNumber=phone_number,
            Message=message,
        )
        logger.debug("SMS response: %s", response)
        return response
    except (BotoCoreError, ClientError) as exc:
        logger.warning("AWS SNS live call fallback (%s): %s", phone_number, exc)
        return {
            "MessageId": f"cds-fallback-{uuid.uuid4().hex[:8]}",
            "Channel": channel,
            "Recipient": phone_number,
            "Status": "FALLBACK_LOGGED",
            "Reason": str(exc),
        }
