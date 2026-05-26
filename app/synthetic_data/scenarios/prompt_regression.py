from datetime import datetime, timedelta, timezone
from app.synthetic_data.scenarios.base import BaseScenario
from app.synthetic_data.templates import cloudwatch, langfuse, hangfire, teams, deployment

SERVICE = "claims-agent"


class PromptRegressionScenario(BaseScenario):
    name = "prompt_regression"
    service = SERVICE

    def generate(self) -> list[dict]:
        now = datetime.now(tz=timezone.utc)
        t_deploy = now - timedelta(minutes=5)
        t_errors = now - timedelta(minutes=3)
        t_retries = now - timedelta(minutes=2)
        t_teams = now - timedelta(minutes=1)
        trace_id = "trace-pr-001"
        dep_id = "dep-33"

        return [
            self._wrap("deployment", deployment.event(SERVICE, "v44", dep_id, t_deploy)),
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "Prompt version change causing increased latency",
                trace_id=trace_id, deployment_id=dep_id, timestamp=t_errors,
            )),
            self._wrap("langfuse", langfuse.latency_spike_trace(
                prompt_version="v44", latency_ms=4200, trace_id=trace_id, timestamp=t_errors,
            )),
            self._wrap("cloudwatch", cloudwatch.error_log(
                SERVICE, "Model response timeout after prompt update",
                deployment_id=dep_id, timestamp=t_errors + timedelta(seconds=30),
            )),
            self._wrap("hangfire", hangfire.failed_log(
                queue="claims", retry_count=4,
                error_message="LLM timeout after prompt change", timestamp=t_retries,
            )),
            self._wrap("teams", teams.message(
                "Ali", "Seeing latency spike after prompt deploy, anyone else?", t_teams,
            )),
            self._wrap("teams", teams.message(
                "Sara", "Confirmed, started after v44 deploy. Rollback?", now,
            )),
        ]
