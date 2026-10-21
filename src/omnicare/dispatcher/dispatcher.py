# ==============================================================================
# File: src/omnicare/dispatcher/dispatcher.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Omnichannel Conversation Router normalizing SMS, RCS, WhatsApp,
#              and Amazon SES Email into a single persistent conversation_id,
#              supporting intent-based channel switching, AxisOS Sovereign Triad
#              edge execution, Care tentacles, and Amazon Bedrock AgentCore.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Unified Care tentacles, AxisOS Edge Bridge, RCS
#     ingress, and SummaryAgent channel switching with persistent state.
# ==============================================================================

import logging
from typing import Any, Dict

from omnicare.agent.loader import run_agentcore
from omnicare.channels.email import send_email
from omnicare.dispatcher.state import get_or_create_state, record_turn
from omnicare.tentacles.appointments import handle_appointment
from omnicare.tentacles.axisos_bridge import (
    handle_axisos,
    read_live_machine_telemetry,
)
from omnicare.tentacles.echo import handle_echo
from omnicare.tentacles.followups import handle_followup
from omnicare.tentacles.help import handle_help
from omnicare.tentacles.medication import handle_medication
from omnicare.utils.serializers import derive_conversation_id

logger = logging.getLogger(__name__)

SUPPORTED_CHANNELS = {"sms", "rcs", "whatsapp", "email"}


def handle_inbound_message(channel: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Primary omnichannel router entrypoint for SMS, RCS, WhatsApp, and Email.
    """
    norm_channel = (channel or "").strip().lower()
    logger.info("Dispatcher received message from channel '%s': %s", norm_channel, payload)

    if norm_channel not in SUPPORTED_CHANNELS:
        logger.warning("Unknown channel '%s'", channel)
        return {"status": "ignored", "reason": "unknown_channel"}

    normalized = normalize_message(norm_channel, payload)

    if norm_channel in ("sms", "rcs"):
        return handle_sms(normalized)
    if norm_channel == "whatsapp":
        return handle_whatsapp(normalized)
    if norm_channel == "email":
        return handle_email(normalized)

    return {"status": "ignored", "reason": "unknown_channel"}


def normalize_message(channel: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes channel-specific webhook payloads into the unified OmniCare
    envelope while preserving a single cross-channel `conversation_id`.
    """
    user_key = (
        payload.get("user_id")
        or payload.get("phone_number")
        or payload.get("wa_id")
        or payload.get("from_address")
        or "anonymous"
    )
    conv_id = payload.get("conversation_id") or derive_conversation_id(str(user_key))

    if channel in ("sms", "rcs"):
        return {
            "conversation_id": conv_id,
            "user_id": user_key,
            "channel": channel,
            "sender": payload.get("phone_number"),
            "text": payload.get("text") or "",
            "timestamp": payload.get("timestamp"),
            "message_id": payload.get("message_id"),
            "email_fallback": payload.get("email", "operator@axisos.pro"),
        }

    if channel == "whatsapp":
        return {
            "conversation_id": conv_id,
            "user_id": user_key,
            "channel": "whatsapp",
            "sender": payload.get("wa_id"),
            "text": payload.get("text") or "",
            "timestamp": payload.get("timestamp"),
            "message_id": payload.get("message_id"),
            "email_fallback": payload.get("email", "operator@axisos.pro"),
        }

    if channel == "email":
        return {
            "conversation_id": conv_id,
            "user_id": user_key,
            "channel": "email",
            "sender": payload.get("from_address"),
            "subject": payload.get("subject"),
            "text": payload.get("body") or payload.get("text") or "",
            "timestamp": payload.get("timestamp"),
            "message_id": payload.get("message_id"),
        }

    return payload


def _route_normalized(msg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core intent router across Care tentacles, AxisOS Edge tentacles,
    SummaryAgent channel switching, and Amazon Bedrock AgentCore.
    """
    channel = msg.get("channel", "sms")
    conv_id = msg.get("conversation_id") or derive_conversation_id(msg.get("sender") or "anon")
    user_id = msg.get("user_id") or msg.get("sender") or "anonymous"
    raw_text = msg.get("text") or ""
    text = raw_text.lower().strip()

    get_or_create_state(str(user_id), channel, conversation_id=conv_id)

    # 1. Intent-based Channel Switch: SMS/WhatsApp -> Amazon SES Email for long-form reports
    if "diagnostic report" in text or ("send" in text and "report" in text):
        telemetry = read_live_machine_telemetry()
        recipient_email = msg.get("email_fallback") or "operator@axisos.pro"
        subject = f"AxisOS Sovereign Triad Diagnostic Report [{conv_id}]"
        report_body = (
            f"Crusan & Co. — AxisOS Sovereign Triad Full Diagnostic Report\n"
            f"Conversation ID: {conv_id}\n"
            f"Originating Channel: {channel.upper()}\n"
            f"RAMGAK Bracket Status: {telemetry.get('ramgak_zone')}\n"
            f"1-Min Load Average: {telemetry.get('load_1m')}\n"
            f"Memory Usage: {telemetry.get('mem_used_mb', 0)} MB / {telemetry.get('mem_total_mb', 0)} MB\n"
            f"SoC Thermal: {telemetry.get('soc_temp_c')} C\n"
            f"Active Network Interfaces: {', '.join(telemetry.get('interfaces', {}).keys())}\n"
        )
        ses_receipt = send_email(recipient_email, subject, report_body)
        result = {
            "tentacle": "channel_switch",
            "agent": "SummaryAgent",
            "conversation_id": conv_id,
            "switched_from": channel,
            "switched_to": "email",
            "ses_dispatch": ses_receipt,
            "response": (
                f"Switched channel from {channel.upper()} to Email ({recipient_email}) "
                f"for full AxisOS diagnostic report [{ses_receipt.get('MessageId')}]."
            ),
        }
        record_turn(
            conv_id,
            channel,
            raw_text,
            "SummaryAgent",
            result["response"],
            switched_to_channel="email",
        )
        return result

    # 2. Care Tentacles (Follow-ups, Appointments, Medication)
    if "followup" in text or "follow up" in text or "follow-up" in text:
        res = handle_followup(msg)
        res["conversation_id"] = conv_id
        record_turn(conv_id, channel, raw_text, "followups", res["response"])
        return res

    if "appointment" in text or "schedule" in text:
        res = handle_appointment(msg)
        res["conversation_id"] = conv_id
        record_turn(conv_id, channel, raw_text, "appointments", res["response"])
        return res

    if "medication" in text or "refill" in text or "prescription" in text:
        res = handle_medication(msg)
        res["conversation_id"] = conv_id
        record_turn(conv_id, channel, raw_text, "medication", res["response"])
        return res

    # 3. AxisOS Sovereign Triad Edge Tentacle (Status, Telemetry, Restart/Checkpoint)
    if any(
        kw in text
        for kw in ("device", "status", "telemetry", "axisos", "triad", "restart", "reboot", "checkpoint")
    ):
        res = handle_axisos(msg)
        res["conversation_id"] = conv_id
        record_turn(conv_id, channel, raw_text, "axisos", res["response"])
        return res

    # 4. Utility Tentacles (Help & Echo)
    if text == "help" or text.startswith("help "):
        res = handle_help(msg)
        res["conversation_id"] = conv_id
        record_turn(conv_id, channel, raw_text, "help", res["response"])
        return res

    if text.startswith("echo "):
        res = handle_echo(msg)
        res["conversation_id"] = conv_id
        record_turn(conv_id, channel, raw_text, "echo", res["response"])
        return res

    # 5. Escalate to Amazon Bedrock AgentCore if no specific tentacle matched
    agent_res = run_agentcore(raw_text)
    agent_res["conversation_id"] = conv_id
    record_turn(
        conv_id,
        channel,
        raw_text,
        agent_res.get("agent", "CareAgent"),
        str(agent_res.get("agentcore_response", "")),
    )
    return agent_res


def handle_sms(msg: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Handling SMS/RCS message: %s", msg)
    return _route_normalized(msg)


def handle_whatsapp(msg: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Handling WhatsApp message: %s", msg)
    return _route_normalized(msg)


def handle_email(msg: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Handling Email message: %s", msg)
    return _route_normalized(msg)
