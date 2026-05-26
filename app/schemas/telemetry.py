from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CloudWatchLog(BaseModel):
    timestamp: datetime
    service: str
    severity: str
    message: str
    trace_id: Optional[str] = None
    deployment_id: Optional[str] = None
    environment: str = "prod"


class LangfuseTrace(BaseModel):
    trace_id: str
    prompt_version: str
    latency_ms: int
    token_input: int
    token_output: int
    model: str
    status: str
    cost: float
    timestamp: datetime


class HangfireLog(BaseModel):
    job_id: str
    queue: str
    retry_count: int
    status: str
    error_message: Optional[str] = None
    timestamp: datetime


class TeamsMessage(BaseModel):
    sender: str
    channel: str
    timestamp: datetime
    message: str


class DeploymentEvent(BaseModel):
    deployment_id: str
    service: str
    version: str
    deployed_at: datetime
