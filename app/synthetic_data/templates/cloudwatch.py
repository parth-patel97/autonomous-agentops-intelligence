import random
import uuid
from datetime import datetime, timezone
from app.schemas.telemetry import CloudWatchLog

SERVICES = ["claims-agent", "auth-service", "policy-service", "notification-service"]

_NORMAL_MESSAGES = [
    "Request processed successfully",
    "Cache hit for key",
    "Scheduled job completed",
    "Health check OK",
    "Token count within limits",
]


def normal_log(service: str | None = None) -> CloudWatchLog:
    return CloudWatchLog(
        timestamp=datetime.now(tz=timezone.utc),
        service=service or random.choice(SERVICES),
        severity=random.choice(["INFO", "INFO", "INFO", "DEBUG", "WARNING"]),
        message=random.choice(_NORMAL_MESSAGES),
        trace_id=f"trace-{uuid.uuid4().hex[:8]}",
        environment="prod",
    )


def error_log(
    service: str,
    message: str,
    trace_id: str | None = None,
    deployment_id: str | None = None,
    timestamp: datetime | None = None,
) -> CloudWatchLog:
    return CloudWatchLog(
        timestamp=timestamp or datetime.now(tz=timezone.utc),
        service=service,
        severity="ERROR",
        message=message,
        trace_id=trace_id or f"trace-{uuid.uuid4().hex[:8]}",
        deployment_id=deployment_id,
        environment="prod",
    )


def warning_log(
    service: str,
    message: str,
    timestamp: datetime | None = None,
) -> CloudWatchLog:
    return CloudWatchLog(
        timestamp=timestamp or datetime.now(tz=timezone.utc),
        service=service,
        severity="WARNING",
        message=message,
        trace_id=f"trace-{uuid.uuid4().hex[:8]}",
        environment="prod",
    )
