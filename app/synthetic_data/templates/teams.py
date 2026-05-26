from datetime import datetime, timezone
from app.schemas.telemetry import TeamsMessage

CHANNEL = "ai-prod"


def message(sender: str, text: str, timestamp: datetime | None = None) -> TeamsMessage:
    return TeamsMessage(
        sender=sender,
        channel=CHANNEL,
        timestamp=timestamp or datetime.now(tz=timezone.utc),
        message=text,
    )
