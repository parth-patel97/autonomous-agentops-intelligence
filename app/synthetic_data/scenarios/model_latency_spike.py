from datetime import datetime, timedelta, timezone
from app.synthetic_data.scenarios.base import BaseScenario
from app.synthetic_data.templates import cloudwatch, langfuse, teams

SERVICE = "claims-agent"


class ModelLatencySpikeScenario(BaseScenario):
    name = "model_latency_spike"
    service = SERVICE

    def generate(self) -> list[dict]:
        now = datetime.now(tz=timezone.utc)
        t0 = now - timedelta(minutes=4)

        return [
            self._wrap("langfuse", langfuse.latency_spike_trace(
                latency_ms=4800, timestamp=t0,
            )),
            self._wrap("langfuse", langfuse.latency_spike_trace(
                latency_ms=5200, timestamp=t0 + timedelta(minutes=1),
            )),
            self._wrap("langfuse", langfuse.latency_spike_trace(
                latency_ms=6100, timestamp=t0 + timedelta(minutes=2),
            )),
            self._wrap("cloudwatch", cloudwatch.warning_log(
                SERVICE, "Model response time 5x above baseline",
                timestamp=t0 + timedelta(minutes=1),
            )),
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "Request timeout: model response exceeded 5000ms",
                timestamp=t0 + timedelta(minutes=2),
            )),
            self._wrap("teams", teams.message(
                "Sam", "Model is extremely slow today — 5x normal latency on claims-agent", now,
            )),
        ]
