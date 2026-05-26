from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.synthetic_data.generator import TelemetryGenerator

router = APIRouter()
_generator = TelemetryGenerator()


class SimulateRequest(BaseModel):
    scenario: str


@router.post("/simulate-incident", status_code=202)
async def simulate_incident(body: SimulateRequest):
    try:
        events = _generator.get_scenario_events(body.scenario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"accepted": True, "scenario": body.scenario, "event_count": len(events)}
