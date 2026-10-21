# ==============================================================================
# File: Dockerfile
# Project: AxisOS OmniCare (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Container build specification for the OmniCare AWS CDS &
#              Bedrock AgentCore omnichannel router and AxisOS Edge Bridge.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Created production Dockerfile for OmniCare API.
# ==============================================================================
FROM python:3.11-slim

LABEL maintainer="Marc F. Crusan / Crusan & Co. w/ AGY"
LABEL org.opencontainers.image.title="AxisOS OmniCare"
LABEL org.opencontainers.image.description="Unified AWS CDS Omnichannel Router + Bedrock AgentCore + AxisOS Edge Control Plane"
LABEL org.opencontainers.image.vendor="Crusan & Co."

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    AGENTCORE_CONFIG_PATH=/app/src/omnicare/agent/agentcore.yaml \
    APP_PORT=8000

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/
COPY server/ /app/server/
COPY infra/ /app/infra/
COPY scripts/ /app/scripts/
COPY README.md LICENSE /app/

EXPOSE 8000

CMD ["uvicorn", "omnicare.main:app", "--host", "0.0.0.0", "--port", "8000"]
