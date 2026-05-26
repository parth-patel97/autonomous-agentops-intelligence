from datetime import datetime, timedelta, timezone
from app.synthetic_data.scenarios.base import BaseScenario
from app.synthetic_data.templates import cloudwatch, langfuse, hangfire, teams

SERVICE = "claims-agent"


class RetryStormScenario(BaseScenario):
    name = "retry_storm"
    service = SERVICE

    def generate(self) -> list[dict]:
        now = datetime.now(tz=timezone.utc)
        t0 = now - timedelta(minutes=5)

        events = []
        for i, retry_count in enumerate([3, 4, 5, 6, 7]):
            events.append(self._wrap("hangfire", hangfire.failed_log(
                queue="claims", retry_count=retry_count,
                error_message="Downstream LLM call failed",
                timestamp=t0 + timedelta(minutes=i),
            )))

        events += [
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "Job retry limit exceeded — queue saturation",
                timestamp=t0 + timedelta(minutes=3),
            )),
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "Queue depth critical: 500+ pending jobs",
                timestamp=t0 + timedelta(minutes=4),
            )),
            self._wrap("langfuse", langfuse.latency_spike_trace(
                latency_ms=3800, timestamp=t0 + timedelta(minutes=2),
            )),
            self._wrap("teams", teams.message(
                "Ops", "Jobs keep failing and retrying — queue is completely backed up", now,
            )),
        ]
        return events
