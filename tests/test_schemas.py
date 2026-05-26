from datetime import datetime, timezone
from app.schemas.telemetry import CloudWatchLog, LangfuseTrace, HangfireLog, TeamsMessage, DeploymentEvent
from app.schemas.trigger import TriggerReason, TriggerEvent
from app.schemas.incident import RCAOutput, Incident


def test_cloudwatch_log():
    log = CloudWatchLog(timestamp=datetime.now(tz=timezone.utc), service="claims-agent", severity="ERROR", message="context_length_exceeded", trace_id="trace-123", deployment_id="dep-33")
    assert log.severity == "ERROR"


def test_langfuse_trace():
    trace = LangfuseTrace(trace_id="trace-123", prompt_version="v44", latency_ms=4100, token_input=23000, token_output=1200, model="qwen3", status="failure", cost=0.02, timestamp=datetime.now(tz=timezone.utc))
    assert trace.latency_ms == 4100


def test_hangfire_log():
    log = HangfireLog(job_id="job-11", queue="claims", retry_count=4, status="failed", error_message="context_length_exceeded", timestamp=datetime.now(tz=timezone.utc))
    assert log.retry_count == 4


def test_teams_message():
    msg = TeamsMessage(sender="Ali", channel="ai-prod", timestamp=datetime.now(tz=timezone.utc), message="Seeing latency spike")
    assert msg.sender == "Ali"


def test_deployment_event():
    event = DeploymentEvent(deployment_id="dep-33", service="claims-agent", version="v44", deployed_at=datetime.now(tz=timezone.utc))
    assert event.version == "v44"


def test_trigger_event():
    event = TriggerEvent(incident_id="INC-001", service="claims-agent", trigger_reason=TriggerReason.LATENCY_SPIKE, triggered_at=datetime.now(tz=timezone.utc))
    assert event.trigger_reason == TriggerReason.LATENCY_SPIKE


def test_rca_output():
    rca = RCAOutput(root_cause="Prompt regression", confidence=89, recommendation="Rollback v44", evidence=["deployment v44", "latency increase"])
    assert rca.confidence == 89


def test_incident():
    incident = Incident(
        incident_id="INC-001", service="claims-agent", trigger_reason=TriggerReason.LATENCY_SPIKE,
        rca=RCAOutput(root_cause="Prompt regression", confidence=89, recommendation="Rollback v44", evidence=[]),
        created_at=datetime.now(tz=timezone.utc),
    )
    assert incident.incident_id == "INC-001"
