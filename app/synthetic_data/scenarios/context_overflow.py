from datetime import datetime, timedelta, timezone
from app.synthetic_data.scenarios.base import BaseScenario
from app.synthetic_data.templates import cloudwatch, langfuse, hangfire, teams

SERVICE = "claims-agent"


class ContextOverflowScenario(BaseScenario):
    name = "context_overflow"
    service = SERVICE

    def generate(self) -> list[dict]:
        now = datetime.now(tz=timezone.utc)
        t0 = now - timedelta(minutes=4)

        return [
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "context_length_exceeded", timestamp=t0,
            )),
            self._wrap("langfuse", langfuse.latency_spike_trace(
                latency_ms=1200, timestamp=t0 + timedelta(seconds=10),
            )),
            self._wrap("hangfire", hangfire.failed_log(
                queue="claims", retry_count=5,
                error_message="context_length_exceeded",
                timestamp=t0 + timedelta(minutes=1),
            )),
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "context_length_exceeded — retry attempt 5",
                timestamp=t0 + timedelta(minutes=2),
            )),
            self._wrap("hangfire", hangfire.failed_log(
                queue="claims", retry_count=6,
                error_message="context_length_exceeded — queue backing up",
                timestamp=t0 + timedelta(minutes=3),
            )),
            self._wrap("teams", teams.message(
                "Dev", "Getting context overflow errors on claims processor", now,
            )),
        ]
