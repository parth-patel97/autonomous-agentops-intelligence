from fastapi import FastAPI
from app.api.incidents import router as incidents_router
from app.api.telemetry import router as telemetry_router
from app.api.metrics import router as metrics_router
from app.api.simulation import router as simulation_router

app = FastAPI(
    title="Autonomous AgentOps Intelligence",
    version="0.1.0",
)

app.include_router(incidents_router)
app.include_router(telemetry_router)
app.include_router(metrics_router)
app.include_router(simulation_router)
