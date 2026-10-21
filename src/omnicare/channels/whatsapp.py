# ==============================================================================
# File: src/omnicare/channels/whatsapp.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: AWS End User Messaging Social (WhatsApp Business Platform)
#              outbound message and Meta Template dispatcher.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented WhatsApp text and Meta template sender.
# ==============================================================================

import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

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


def _get_whatsapp_client():
    region = os.getenv("AWS_REGION", "us-west-2")
    boto_config = Config(
        region_name=region,
        retries={"max_attempts": 3, "mode": "standard"},
    )
    return boto3.client("socialmessaging", config=boto_config)


def _has_live_aws_credentials() -> bool:
    key = os.getenv("AWS_ACCESS_KEY_ID", "")
    return bool(key and key != "your_access_key_id_here")


def send_whatsapp(
    wa_id: str,
    message: str,
    template_name: Optional[str] = None,
    template_params: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Dispatches an outbound WhatsApp message or approved Meta WhatsApp Template
    via AWS End User Messaging Social (`socialmessaging`).
    """
    origination_id = os.getenv("CDS_WHATSAPP_PHONE_NUMBER_ID", "waba-phone-id-001")
    logger.info(
        "Sending WhatsApp to %s (template=%s)",
        wa_id,
        template_name or "freeform_text",
    )

    if template_name:
        meta_payload = {
            "messaging_product": "whatsapp",
            "to": wa_id,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "en_US"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": str(p)}
                            for p in (template_params or [])
                        ],
                    }
                ],
            },
        }
    else:
        meta_payload = {
            "messaging_product": "whatsapp",
            "to": wa_id,
            "type": "text",
            "text": {"preview_url": False, "body": message},
        }

    if not _has_live_aws_credentials():
        msg_id = f"wamid.{uuid.uuid4().hex[:16]}"
        return {
            "messageId": msg_id,
            "channel": "whatsapp",
            "recipient": wa_id,
            "template": template_name,
            "meta_payload": meta_payload,
            "status": "DISPATCHED_AUDIT",
        }

    try:
        client = _get_whatsapp_client()
        response = client.send_whatsapp_message(
            originationPhoneNumberId=origination_id,
            message=json.dumps(meta_payload).encode("utf-8"),
            metaApiVersion="v20.0",
        )
        return response
    except (BotoCoreError, ClientError, Exception) as exc:
        logger.warning("AWS WhatsApp live call fallback (%s): %s", wa_id, exc)
        return {
            "messageId": f"wamid.fallback.{uuid.uuid4().hex[:10]}",
            "channel": "whatsapp",
            "recipient": wa_id,
            "template": template_name,
            "status": "FALLBACK_LOGGED",
            "reason": str(exc),
        }
