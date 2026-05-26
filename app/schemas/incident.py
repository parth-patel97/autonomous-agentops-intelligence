from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.trigger import TriggerReason


class RCAOutput(BaseModel):
    root_cause: str
    confidence: int
    recommendation: str
    evidence: List[str]


class Incident(BaseModel):
    incident_id: str
    service: str
    trigger_reason: TriggerReason
    rca: RCAOutput
    created_at: datetime
    resolved: bool = False
    raw_evidence: List[dict] = []
