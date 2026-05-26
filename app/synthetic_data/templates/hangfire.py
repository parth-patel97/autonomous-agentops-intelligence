import uuid
from datetime import datetime, timezone
from app.schemas.telemetry import HangfireLog

QUEUES = ["claims", "policy", "notifications", "audit"]


def normal_log(queue: str = "claims") -> HangfireLog:
    return HangfireLog(
        job_id=f"job-{uuid.uuid4().hex[:6]}",
        queue=queue,
        retry_count=0,
        status="succeeded",
        timestamp=datetime.now(tz=timezone.utc),
    )


def failed_log(
    queue: str = "claims",
    retry_count: int = 4,
    error_message: str = "LLM call failed",
    timestamp: datetime | None = None,
) -> HangfireLog:
    return HangfireLog(
        job_id=f"job-{uuid.uuid4().hex[:6]}",
        queue=queue,
        retry_count=retry_count,
        status="failed",
        error_message=error_message,
        timestamp=timestamp or datetime.now(tz=timezone.utc),
    )
