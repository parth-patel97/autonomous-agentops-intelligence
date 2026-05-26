from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

VALID_SCENARIOS = {
    "prompt_regression",
    "context_overflow",
    "retry_storm",
    "cost_explosion",
    "model_latency_spike",
}


class SimulateRequest(BaseModel):
    scenario: str


@router.post("/simulate-incident", status_code=202)
async def simulate_incident(body: SimulateRequest):
    if body.scenario not in VALID_SCENARIOS:
        raise HTTPException(status_code=400, detail=f"Unknown scenario: {body.scenario}")
    return {"accepted": True, "scenario": body.scenario}
