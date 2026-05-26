from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TriggerReason(str, Enum):
    LATENCY_SPIKE = "latency_spike"
    ERROR_SPIKE = "error_spike"
    RETRY_SPIKE = "retry_spike"
    COST_SPIKE = "cost_spike"
    TOKEN_SPIKE = "token_spike"


class TriggerEvent(BaseModel):
    incident_id: str
    service: str
    trigger_reason: TriggerReason
    triggered_at: datetime
    metadata: dict = {}
