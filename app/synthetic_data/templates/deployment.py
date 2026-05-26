from datetime import datetime, timezone
from app.schemas.telemetry import DeploymentEvent


def event(
    service: str,
    version: str,
    deployment_id: str,
    deployed_at: datetime | None = None,
) -> DeploymentEvent:
    return DeploymentEvent(
        deployment_id=deployment_id,
        service=service,
        version=version,
        deployed_at=deployed_at or datetime.now(tz=timezone.utc),
    )
