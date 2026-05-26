import pytest
from app.synthetic_data.generator import TelemetryGenerator
from app.synthetic_data.scenarios.prompt_regression import PromptRegressionScenario
from app.synthetic_data.scenarios.context_overflow import ContextOverflowScenario
from app.synthetic_data.scenarios.retry_storm import RetryStormScenario
from app.synthetic_data.scenarios.cost_explosion import CostExplosionScenario
from app.synthetic_data.scenarios.model_latency_spike import ModelLatencySpikeScenario
from app.trigger_engine.rules import LATENCY_BASELINE_MS, LATENCY_MULTIPLIER

SOURCE_TYPES = {"cloudwatch", "langfuse", "hangfire", "teams", "deployment"}


def _assert_events(events: list[dict], min_count: int = 1):
    assert len(events) >= min_count
    for e in events:
        assert "_source_type" in e
        assert e["_source_type"] in SOURCE_TYPES


def test_prompt_regression_events():
    events = PromptRegressionScenario().generate()
    _assert_events(events, min_count=6)
    source_types = {e["_source_type"] for e in events}
    assert "deployment" in source_types
    assert "langfuse" in source_types
    assert "teams" in source_types
    # latency must exceed threshold
    langfuse_events = [e for e in events if e["_source_type"] == "langfuse"]
    assert any(e["latency_ms"] > LATENCY_BASELINE_MS * LATENCY_MULTIPLIER for e in langfuse_events)


def test_context_overflow_events():
    events = ContextOverflowScenario().generate()
    _assert_events(events, min_count=5)
    cw_errors = [e for e in events if e["_source_type"] == "cloudwatch"]
    assert any("context_length_exceeded" in e["message"] for e in cw_errors)
    hf_events = [e for e in events if e["_source_type"] == "hangfire"]
    assert any(e["retry_count"] >= 5 for e in hf_events)


def test_retry_storm_events():
    events = RetryStormScenario().generate()
    _assert_events(events, min_count=7)
    hf_events = [e for e in events if e["_source_type"] == "hangfire"]
    assert len(hf_events) >= 5
    retry_counts = [e["retry_count"] for e in hf_events]
    assert max(retry_counts) >= 6


def test_cost_explosion_events():
    events = CostExplosionScenario().generate()
    _assert_events(events, min_count=4)
    lf_events = [e for e in events if e["_source_type"] == "langfuse"]
    assert any(e["token_input"] >= 40000 for e in lf_events)
    assert any(e["cost"] > 0.1 for e in lf_events)


def test_model_latency_spike_events():
    events = ModelLatencySpikeScenario().generate()
    _assert_events(events, min_count=5)
    lf_events = [e for e in events if e["_source_type"] == "langfuse"]
    assert any(e["latency_ms"] > LATENCY_BASELINE_MS * 4 for e in lf_events)


def test_generator_knows_all_scenarios():
    gen = TelemetryGenerator()
    expected = {"prompt_regression", "context_overflow", "retry_storm", "cost_explosion", "model_latency_spike"}
    assert set(gen.scenario_names) == expected


def test_generator_get_scenario_events():
    gen = TelemetryGenerator()
    events = gen.get_scenario_events("context_overflow")
    assert len(events) > 0


def test_generator_unknown_scenario_raises():
    gen = TelemetryGenerator()
    with pytest.raises(ValueError, match="Unknown scenario"):
        gen.get_scenario_events("nonexistent")


@pytest.mark.anyio
async def test_generator_stream_yields_events():
    gen = TelemetryGenerator()
    events = []
    async for event in gen.stream():
        events.append(event)
        if len(events) >= 5:
            break
    assert len(events) == 5
    for e in events:
        assert "_source_type" in e
