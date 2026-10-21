# ==============================================================================
# File: src/omnicare/server/api.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Unified AWS CDS inbound webhook endpoints for SMS, RCS, WhatsApp,
#              and Amazon SES Email, plus AxisOS Edge status/action endpoints.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Added RCS route, Pydantic v1/v2 compatibility, and
#     AxisOS Sovereign Triad endpoints.
# ==============================================================================

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from omnicare.dispatcher.dispatcher import handle_inbound_message
from omnicare.heartbeat.heartbeat import collect_triad_heartbeat
from omnicare.tentacles.axisos_bridge import handle_axisos

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["cds-webhooks"])


def _model_to_dict(model: BaseModel) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


class InboundSMS(BaseModel):
    message_id: str
    phone_number: str
    text: str
    timestamp: str
    email: Optional[str] = "operator@axisos.pro"


class InboundWhatsApp(BaseModel):
    message_id: str
    wa_id: str
    text: str
    timestamp: str
    email: Optional[str] = "operator@axisos.pro"


class InboundEmail(BaseModel):
    message_id: str
    from_address: str
    subject: str
    body: str
    timestamp: str


class AxisOSTaskRequest(BaseModel):
    edge_id: str = "pp-core-pri"
    command: str = "status"


@router.post("/sms")
async def sms_webhook(payload: InboundSMS):
    try:
        logger.info("Inbound SMS: %s", payload)
        return handle_inbound_message("sms", _model_to_dict(payload))
    except Exception as exc:
        logger.error("SMS webhook error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/rcs")
async def rcs_webhook(payload: InboundSMS):
    try:
        logger.info("Inbound RCS: %s", payload)
        return handle_inbound_message("rcs", _model_to_dict(payload))
    except Exception as exc:
        logger.error("RCS webhook error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/whatsapp")
async def whatsapp_webhook(payload: InboundWhatsApp):
    try:
        logger.info("Inbound WhatsApp: %s", payload)
        return handle_inbound_message("whatsapp", _model_to_dict(payload))
    except Exception as exc:
        logger.error("WhatsApp webhook error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/email")
async def email_webhook(payload: InboundEmail):
    try:
        logger.info("Inbound Email: %s", payload)
        return handle_inbound_message("email", _model_to_dict(payload))
    except Exception as exc:
        logger.error("Email webhook error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/axisos/status")
async def axisos_status():
    return collect_triad_heartbeat(probe_network=False)


@router.post("/axisos/run_task")
async def axisos_run_task(req: AxisOSTaskRequest):
    return handle_axisos({"text": req.command, "edge_id": req.edge_id})
