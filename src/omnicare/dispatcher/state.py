# ==============================================================================
# File: src/omnicare/dispatcher/state.py
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Cross-channel conversation state manager backed by DynamoDB
#              schema with deterministic in-memory continuity cache.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Implemented unified conversation_id state store.
# ==============================================================================

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from omnicare.utils.serializers import derive_conversation_id

_CONVERSATION_STORE: Dict[str, Dict[str, Any]] = {}


def get_or_create_state(
    user_id: str,
    channel: str,
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Loads or initializes the unified conversation state for `conversation_id`.
    Matches the DynamoDB schema (`conversation_id` PK, `user_id`,
    `last_agent_state`, `preferred_channel`, `axisos_edge_refs`, `history`).
    """
    conv_id = conversation_id or derive_conversation_id(user_id)
    now = datetime.now(timezone.utc).isoformat()

    if conv_id not in _CONVERSATION_STORE:
        _CONVERSATION_STORE[conv_id] = {
            "conversation_id": conv_id,
            "user_id": user_id,
            "last_agent_state": "IDLE",
            "preferred_channel": channel,
            "channels_seen": [channel],
            "axisos_edge_refs": ["pp-core-pri", "outpost-cloud-01"],
            "history": [],
            "updated_at": now,
        }
    else:
        state = _CONVERSATION_STORE[conv_id]
        if channel not in state["channels_seen"]:
            state["channels_seen"].append(channel)
        state["updated_at"] = now

    return _CONVERSATION_STORE[conv_id]


def record_turn(
    conversation_id: str,
    channel: str,
    inbound_text: str,
    agent_or_tentacle: str,
    response_text: str,
    switched_to_channel: Optional[str] = None,
) -> Dict[str, Any]:
    state = _CONVERSATION_STORE.get(conversation_id)
    if not state:
        state = get_or_create_state(conversation_id, channel, conversation_id=conversation_id)

    state["last_agent_state"] = agent_or_tentacle
    if switched_to_channel:
        state["preferred_channel"] = switched_to_channel
        if switched_to_channel not in state["channels_seen"]:
            state["channels_seen"].append(switched_to_channel)

    turn_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "switched_to": switched_to_channel,
        "inbound": inbound_text,
        "handler": agent_or_tentacle,
        "response": response_text,
    }
    history: List[Dict[str, Any]] = state.setdefault("history", [])
    history.append(turn_entry)
    return state


def clear_state_store() -> None:
    _CONVERSATION_STORE.clear()
