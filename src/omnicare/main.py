# ==============================================================================
# File: src/omnicare/main.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: FastAPI application entrypoint integrating AWS Communication
#              Developer Services (CDS), Amazon Bedrock AgentCore, and the
#              AxisOS Sovereign Triad edge layer.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Added WhatsApp/Email outbound routes, AxisOS `/status`
#     and `/run_task` routes, and canonical SOP attribution.
# ==============================================================================

import logging
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from omnicare.channels.email import send_email
from omnicare.channels.sms import send_sms
from omnicare.channels.whatsapp import send_whatsapp
from omnicare.heartbeat.heartbeat import collect_triad_heartbeat
from omnicare.server.api import router as webhook_router
from omnicare.tentacles.axisos_bridge import handle_axisos

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("omnicare.main")

app = FastAPI(
    title="Crusan & Co. — AxisOS OmniCare",
    description=(
        "Unified AWS CDS Omnichannel Control Plane (SMS, RCS, WhatsApp, SES Email) "
        "+ Amazon Bedrock AgentCore + AxisOS Sovereign Triad Edge Integration"
    ),
    version="1.0.0",
)

app.include_router(webhook_router)


class SMSRequest(BaseModel):
    phone_number: str
    message: str


class WhatsAppRequest(BaseModel):
    wa_id: str
    message: str
    template_name: Optional[str] = None
    template_params: Optional[List[str]] = None


class EmailRequest(BaseModel):
    to_address: str
    subject: str
    body_text: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "omnicare",
        "vendor": "Crusan & Co.",
        "platform": "AxisOS OmniCare",
        "pillars": ["HONEST", "AUDITABLE", "OWNED"],
    }


@app.get("/status")
def axisos_edge_status():
    """Returns live AxisOS Sovereign Triad & RAMGAK telemetry."""
    return collect_triad_heartbeat(probe_network=False)


@app.post("/run_task")
def axisos_edge_task(cmd: str = "status"):
    """Executes a verified AxisOS edge task (`status`, `checkpoint`, `reboot_check`)."""
    return handle_axisos({"text": cmd})


@app.post("/sms/send")
def sms_send(req: SMSRequest):
    try:
        logger.info("SMS send request: %s", req)
        response = send_sms(req.phone_number, req.message)
        return {"status": "sent", "aws_response": response}
    except Exception as exc:
        logger.error("SMS send failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/whatsapp/send")
def whatsapp_send(req: WhatsAppRequest):
    try:
        logger.info("WhatsApp send request: %s", req)
        response = send_whatsapp(
            req.wa_id,
            req.message,
            template_name=req.template_name,
            template_params=req.template_params,
        )
        return {"status": "sent", "aws_response": response}
    except Exception as exc:
        logger.error("WhatsApp send failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/email/send")
def email_send(req: EmailRequest):
    try:
        logger.info("Email send request: %s", req)
        response = send_email(req.to_address, req.subject, req.body_text)
        return {"status": "sent", "aws_response": response}
    except Exception as exc:
        logger.error("Email send failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
