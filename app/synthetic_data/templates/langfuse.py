import random
import uuid
from datetime import datetime, timezone
from app.schemas.telemetry import LangfuseTrace

PROMPT_VERSION_NORMAL = "v43"
PROMPT_VERSION_REGRESSED = "v44"


def normal_trace(service: str = "claims-agent", trace_id: str | None = None) -> LangfuseTrace:
    return LangfuseTrace(
        trace_id=trace_id or f"trace-{uuid.uuid4().hex[:8]}",
        prompt_version=PROMPT_VERSION_NORMAL,
        latency_ms=random.randint(600, 900),
        token_input=random.randint(1000, 3000),
        token_output=random.randint(200, 600),
        model="qwen3",
        status="success",
        cost=round(random.uniform(0.001, 0.005), 4),
        timestamp=datetime.now(tz=timezone.utc),
    )


def latency_spike_trace(
    prompt_version: str = PROMPT_VERSION_REGRESSED,
    latency_ms: int = 4200,
    trace_id: str | None = None,
    timestamp: datetime | None = None,
) -> LangfuseTrace:
    return LangfuseTrace(
        trace_id=trace_id or f"trace-{uuid.uuid4().hex[:8]}",
        prompt_version=prompt_version,
        latency_ms=latency_ms,
        token_input=random.randint(15000, 23000),
        token_output=random.randint(800, 1500),
        model="qwen3",
        status="failure",
        cost=round(random.uniform(0.015, 0.025), 4),
        timestamp=timestamp or datetime.now(tz=timezone.utc),
    )


def token_spike_trace(
    token_input: int = 45000,
    token_output: int = 8000,
    timestamp: datetime | None = None,
) -> LangfuseTrace:
    cost = round((token_input + token_output) * 0.000004, 4)
    return LangfuseTrace(
        trace_id=f"trace-{uuid.uuid4().hex[:8]}",
        prompt_version=PROMPT_VERSION_NORMAL,
        latency_ms=random.randint(1800, 2400),
        token_input=token_input,
        token_output=token_output,
        model="qwen3",
        status="success",
        cost=cost,
        timestamp=timestamp or datetime.now(tz=timezone.utc),
    )
