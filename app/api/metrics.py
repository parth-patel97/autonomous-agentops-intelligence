from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
async def get_metrics():
    return {
        "avg_latency_ms": 0,
        "incident_count": 0,
        "retrieval_time_ms": 0,
        "token_reduction_pct": 0,
    }
