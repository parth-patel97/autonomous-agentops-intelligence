import asyncio
import random
from typing import AsyncIterator

from app.synthetic_data.scenarios.prompt_regression import PromptRegressionScenario
from app.synthetic_data.scenarios.context_overflow import ContextOverflowScenario
from app.synthetic_data.scenarios.retry_storm import RetryStormScenario
from app.synthetic_data.scenarios.cost_explosion import CostExplosionScenario
from app.synthetic_data.scenarios.model_latency_spike import ModelLatencySpikeScenario
from app.synthetic_data.templates import cloudwatch, langfuse, hangfire, teams


class TelemetryGenerator:
    def __init__(self):
        self._scenarios = {
            "prompt_regression": PromptRegressionScenario(),
            "context_overflow": ContextOverflowScenario(),
            "retry_storm": RetryStormScenario(),
            "cost_explosion": CostExplosionScenario(),
            "model_latency_spike": ModelLatencySpikeScenario(),
        }

    async def stream(self) -> AsyncIterator[dict]:
        """Yields normal background telemetry events continuously."""
        def _cw():
            return {"_source_type": "cloudwatch", **cloudwatch.normal_log().model_dump(mode="json")}
        def _lf():
            return {"_source_type": "langfuse", **langfuse.normal_trace().model_dump(mode="json")}
        def _hf():
            return {"_source_type": "hangfire", **hangfire.normal_log().model_dump(mode="json")}
        def _tm():
            msgs = ["All good on my end", "Processing looks normal", "Metrics steady"]
            senders = ["Bot", "Monitor", "AutoCheck"]
            return {"_source_type": "teams", **teams.message(
                random.choice(senders), random.choice(msgs)
            ).model_dump(mode="json")}

        _generators = [_cw, _lf, _hf, _tm]
        while True:
            yield random.choice(_generators)()
            await asyncio.sleep(0.5)

    def get_scenario_events(self, name: str) -> list[dict]:
        """Return correlated anomalous events for a named scenario."""
        scenario = self._scenarios.get(name)
        if not scenario:
            raise ValueError(f"Unknown scenario: {name}. Valid: {list(self._scenarios)}")
        return scenario.generate()

    @property
    def scenario_names(self) -> list[str]:
        return list(self._scenarios)
