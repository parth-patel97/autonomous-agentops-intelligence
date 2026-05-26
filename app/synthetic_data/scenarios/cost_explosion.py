from datetime import datetime, timedelta, timezone
from app.synthetic_data.scenarios.base import BaseScenario
from app.synthetic_data.templates import cloudwatch, langfuse, teams

SERVICE = "claims-agent"


class CostExplosionScenario(BaseScenario):
    name = "cost_explosion"
    service = SERVICE

    def generate(self) -> list[dict]:
        now = datetime.now(tz=timezone.utc)
        t0 = now - timedelta(minutes=4)

        return [
            self._wrap("langfuse", langfuse.token_spike_trace(
                token_input=45000, token_output=8000,
                timestamp=t0,
            )),
            self._wrap("langfuse", langfuse.token_spike_trace(
                token_input=52000, token_output=9000,
                timestamp=t0 + timedelta(minutes=1),
            )),
            self._wrap("langfuse", langfuse.token_spike_trace(
                token_input=61000, token_output=11000,
                timestamp=t0 + timedelta(minutes=2),
            )),
            self._wrap("cloudwatch", cloudwatch.warning_log(
                SERVICE, "Token usage 10x above baseline in last 15 minutes",
                timestamp=t0 + timedelta(minutes=2),
            )),
            self._wrap("teams", teams.message(
                "Finance", "Our LLM costs just spiked 10x in the last hour — check claims-agent", now,
            )),
        ]
