# ==============================================================================
# File: src/omnicare/channels/email.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Amazon Simple Email Service (SES) outbound email dispatcher for
#              long-form AxisOS diagnostic reports and channel-switched threads.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented Amazon SES email sender with audit mode.
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


def _get_ses_client():
    region = os.getenv("AWS_REGION", "us-west-2")
    boto_config = Config(
        region_name=region,
        retries={"max_attempts": 3, "mode": "standard"},
    )
    return boto3.client("ses", config=boto_config)


def _has_live_aws_credentials() -> bool:
    key = os.getenv("AWS_ACCESS_KEY_ID", "")
    return bool(key and key != "your_access_key_id_here")


def send_email(to_address: str, subject: str, body_text: str) -> Dict[str, Any]:
    """
    Sends a long-form diagnostic report or follow-up confirmation via Amazon SES.
    """
    from_address = os.getenv("CDS_SES_FROM_EMAIL", "omnicare@axisos.pro")
    logger.info("Sending SES email to %s | Subject: %s", to_address, subject)

    if not _has_live_aws_credentials():
        msg_id = f"ses-{uuid.uuid4().hex[:14]}@us-west-2.amazonses.com"
        return {
            "MessageId": msg_id,
            "Channel": "email",
            "From": from_address,
            "To": to_address,
            "Subject": subject,
            "Status": "DISPATCHED_AUDIT",
        }

    try:
        client = _get_ses_client()
        response = client.send_email(
            Source=from_address,
            Destination={"ToAddresses": [to_address]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Text": {"Data": body_text, "Charset": "UTF-8"}},
            },
        )
        return response
    except (BotoCoreError, ClientError) as exc:
        logger.warning("AWS SES live call fallback (%s): %s", to_address, exc)
        return {
            "MessageId": f"ses-fallback-{uuid.uuid4().hex[:10]}",
            "Channel": "email",
            "To": to_address,
            "Subject": subject,
            "Status": "FALLBACK_LOGGED",
            "Reason": str(exc),
        }
