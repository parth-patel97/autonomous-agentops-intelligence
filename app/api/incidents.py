from fastapi import APIRouter, HTTPException

router = APIRouter()
_incidents: list = []


@router.get("/incidents")
async def get_incidents():
    return _incidents


@router.get("/incident/{incident_id}")
async def get_incident(incident_id: str):
    for inc in _incidents:
        if inc.get("incident_id") == incident_id:
            return inc
    raise HTTPException(status_code=404, detail="Incident not found")
