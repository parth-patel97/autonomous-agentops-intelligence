# Project Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the complete scalable project skeleton for the Autonomous AI Agent Failure Intelligence Platform — all directories, base config, Pydantic schemas, FastAPI app entry point, and Docker Compose.

**Architecture:** Python 3.12 FastAPI monorepo with clear module boundaries (ingestion / trigger / retrieval / agent / api). All inter-module contracts defined via Pydantic schemas upfront so later phases slot in without refactoring. OpenSearch + Ollama run in Docker; FastAPI runs locally via uvicorn.

**Tech Stack:** Python 3.12, FastAPI, Pydantic v2, pydantic-settings, OpenSearch (Docker), Ollama (Docker), pytest, Next.js (dashboard scaffolded separately in Phase 7)

---

## File Map

```
autonomous-agentops-intelligence/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app + router registration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── incidents.py                 # GET /incidents, GET /incident/{id}
│   │   ├── telemetry.py                 # GET /telemetry/live (SSE stub)
│   │   ├── metrics.py                   # GET /metrics
│   │   └── simulation.py               # POST /simulate-incident
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── base.py                      # BaseIngestor ABC
│   ├── synthetic_data/
│   │   ├── __init__.py
│   │   ├── generator.py                 # Generator orchestrator stub
│   │   └── scenarios/
│   │       └── __init__.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── hybrid_search.py             # HybridSearch stub
│   ├── trigger_engine/
│   │   ├── __init__.py
│   │   ├── rules.py                     # Threshold constants
│   │   └── detector.py                  # TriggerDetector stub
│   ├── agent/
│   │   ├── __init__.py
│   │   └── rca_agent.py                 # RCAAgent stub
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── rca_prompt.py                # RCA prompt template string
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── telemetry.py                 # CloudWatchLog, LangfuseTrace, HangfireLog, TeamsMessage, DeploymentEvent
│   │   ├── incident.py                  # IncidentTrigger, RCAOutput, Incident
│   │   └── trigger.py                   # TriggerReason enum, TriggerEvent
│   └── config/
│       ├── __init__.py
│       └── settings.py                  # Settings via pydantic-settings
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # Shared fixtures
│   ├── test_schemas.py                  # Schema validation tests
│   └── test_settings.py                 # Settings load tests
├── docker-compose.yml                   # OpenSearch + OpenSearch Dashboard + Ollama
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Task 1: Python project init + requirements

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`

- [ ] **Step 1: Create requirements.txt**

```text
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.7.4
pydantic-settings==2.3.4
opensearch-py==2.7.1
httpx==0.27.0
python-dotenv==1.0.1
pytest==8.2.2
pytest-asyncio==0.23.7
anyio==4.4.0
```

- [ ] **Step 2: Create .env.example**

```bash
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=admin
OPENSEARCH_PASSWORD=admin
OLLAMA_HOST=http://localhost:11434
EMBED_MODEL=nomic-embed-text
LLM_MODEL=qwen3
EMBED_DIMENSION=768
TRIGGER_LATENCY_MULTIPLIER=3.0
TRIGGER_ERROR_RATE_THRESHOLD=0.3
TRIGGER_RETRY_THRESHOLD=4
TRIGGER_TOKEN_SPIKE_THRESHOLD=20000
```

- [ ] **Step 3: Create .gitignore**

```
__pycache__/
*.py[cod]
.env
.venv/
venv/
*.egg-info/
dist/
.pytest_cache/
.mypy_cache/
node_modules/
.next/
```

- [ ] **Step 4: Create virtual env and install**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Expected: all packages install without error.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .env.example .gitignore
git commit -m "chore: init python project with requirements"
```

---

## Task 2: Docker Compose (OpenSearch + Ollama)

**Files:**
- Create: `docker-compose.yml`

- [ ] **Step 1: Create docker-compose.yml**

```yaml
version: "3.8"

services:
  opensearch:
    image: opensearchproject/opensearch:2.14.0
    container_name: opensearch
    environment:
      - discovery.type=single-node
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=Admin@12345
      - plugins.security.disabled=false
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "9200:9200"
      - "9600:9600"
    volumes:
      - opensearch-data:/usr/share/opensearch/data

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:2.14.0
    container_name: opensearch-dashboards
    ports:
      - "5601:5601"
    environment:
      - OPENSEARCH_HOSTS=["https://opensearch:9200"]
    depends_on:
      - opensearch

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama

volumes:
  opensearch-data:
  ollama-data:
```

- [ ] **Step 2: Start Docker stack**

```bash
docker compose up -d
```

Expected: three containers running. Verify:

```bash
docker compose ps
```

Expected output shows `opensearch`, `opensearch-dashboards`, `ollama` all `running`.

- [ ] **Step 3: Wait for OpenSearch health**

```bash
curl -sk -u admin:Admin@12345 https://localhost:9200/_cluster/health | python3 -m json.tool
```

Expected: `"status": "green"` or `"yellow"` (single-node is yellow, that's fine).

- [ ] **Step 4: Pull Ollama models**

```bash
docker exec ollama ollama pull nomic-embed-text
docker exec ollama ollama pull qwen3:1.7b
```

Expected: both models download successfully.

- [ ] **Step 5: Commit**

```bash
git add docker-compose.yml
git commit -m "chore: add docker compose for opensearch and ollama"
```

---

## Task 3: Config / Settings

**Files:**
- Create: `app/__init__.py`
- Create: `app/config/__init__.py`
- Create: `app/config/settings.py`
- Create: `.env` (from `.env.example` — not committed)
- Test: `tests/test_settings.py`

- [ ] **Step 1: Write failing test**

Create `tests/__init__.py` (empty) and `tests/test_settings.py`:

```python
from app.config.settings import settings


def test_settings_load():
    assert settings.opensearch_host == "localhost"
    assert settings.opensearch_port == 9200
    assert settings.embed_dimension == 768


def test_settings_has_trigger_thresholds():
    assert settings.trigger_latency_multiplier == 3.0
    assert settings.trigger_error_rate_threshold == 0.3
    assert settings.trigger_retry_threshold == 4
    assert settings.trigger_token_spike_threshold == 20000
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_settings.py -v
```

Expected: `ModuleNotFoundError: No module named 'app'`

- [ ] **Step 3: Implement settings**

Create `app/__init__.py` (empty).

Create `app/config/__init__.py` (empty).

Create `app/config/settings.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    opensearch_host: str = "localhost"
    opensearch_port: int = 9200
    opensearch_user: str = "admin"
    opensearch_password: str = "admin"

    ollama_host: str = "http://localhost:11434"
    embed_model: str = "nomic-embed-text"
    llm_model: str = "qwen3"
    embed_dimension: int = 768

    trigger_latency_multiplier: float = 3.0
    trigger_error_rate_threshold: float = 0.3
    trigger_retry_threshold: int = 4
    trigger_token_spike_threshold: int = 20000


settings = Settings()
```

- [ ] **Step 4: Copy .env from example**

```bash
cp .env.example .env
```

- [ ] **Step 5: Run test to verify it passes**

```bash
pytest tests/test_settings.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add app/__init__.py app/config/ tests/__init__.py tests/test_settings.py
git commit -m "feat: add pydantic-settings config with trigger thresholds"
```

---

## Task 4: Pydantic Schemas — Telemetry

**Files:**
- Create: `app/schemas/__init__.py`
- Create: `app/schemas/telemetry.py`
- Test: `tests/test_schemas.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_schemas.py`:

```python
from datetime import datetime, timezone
from app.schemas.telemetry import (
    CloudWatchLog,
    LangfuseTrace,
    HangfireLog,
    TeamsMessage,
    DeploymentEvent,
)


def test_cloudwatch_log_valid():
    log = CloudWatchLog(
        timestamp=datetime.now(tz=timezone.utc),
        service="claims-agent",
        severity="ERROR",
        message="context_length_exceeded",
        trace_id="trace-123",
        deployment_id="dep-33",
        environment="prod",
    )
    assert log.severity == "ERROR"
    assert log.service == "claims-agent"


def test_langfuse_trace_valid():
    trace = LangfuseTrace(
        trace_id="trace-123",
        prompt_version="v44",
        latency_ms=4100,
        token_input=23000,
        token_output=1200,
        model="qwen3",
        status="failure",
        cost=0.02,
        timestamp=datetime.now(tz=timezone.utc),
    )
    assert trace.latency_ms == 4100
    assert trace.token_input == 23000


def test_hangfire_log_valid():
    log = HangfireLog(
        job_id="job-11",
        queue="claims",
        retry_count=4,
        status="failed",
        error_message="context_length_exceeded",
        timestamp=datetime.now(tz=timezone.utc),
    )
    assert log.retry_count == 4


def test_teams_message_valid():
    msg = TeamsMessage(
        sender="Ali",
        channel="ai-prod",
        timestamp=datetime.now(tz=timezone.utc),
        message="Seeing latency spike after prompt deploy",
    )
    assert msg.sender == "Ali"


def test_deployment_event_valid():
    event = DeploymentEvent(
        deployment_id="dep-33",
        service="claims-agent",
        version="v44",
        deployed_at=datetime.now(tz=timezone.utc),
    )
    assert event.version == "v44"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_schemas.py -v
```

Expected: `ModuleNotFoundError: No module named 'app.schemas'`

- [ ] **Step 3: Implement telemetry schemas**

Create `app/schemas/__init__.py` (empty).

Create `app/schemas/telemetry.py`:

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CloudWatchLog(BaseModel):
    timestamp: datetime
    service: str
    severity: str  # DEBUG | INFO | WARNING | ERROR | CRITICAL
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
    status: str  # success | failure
    cost: float
    timestamp: datetime


class HangfireLog(BaseModel):
    job_id: str
    queue: str
    retry_count: int
    status: str  # enqueued | processing | succeeded | failed
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_schemas.py -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/schemas/ tests/test_schemas.py
git commit -m "feat: add pydantic schemas for all telemetry sources"
```

---

## Task 5: Pydantic Schemas — Incident + Trigger

**Files:**
- Create: `app/schemas/trigger.py`
- Create: `app/schemas/incident.py`
- Modify: `tests/test_schemas.py` (append)

- [ ] **Step 1: Write failing tests (append to test_schemas.py)**

Append to `tests/test_schemas.py`:

```python
from app.schemas.trigger import TriggerReason, TriggerEvent
from app.schemas.incident import RCAOutput, Incident


def test_trigger_event_valid():
    event = TriggerEvent(
        incident_id="INC-001",
        service="claims-agent",
        trigger_reason=TriggerReason.LATENCY_SPIKE,
        triggered_at=datetime.now(tz=timezone.utc),
    )
    assert event.trigger_reason == TriggerReason.LATENCY_SPIKE


def test_rca_output_valid():
    rca = RCAOutput(
        root_cause="Prompt regression after v44 deploy",
        confidence=89,
        recommendation="Rollback prompt to v43",
        evidence=["deployment v44", "latency increase", "retry storm"],
    )
    assert rca.confidence == 89
    assert len(rca.evidence) == 3


def test_incident_valid():
    incident = Incident(
        incident_id="INC-001",
        service="claims-agent",
        trigger_reason=TriggerReason.LATENCY_SPIKE,
        rca=RCAOutput(
            root_cause="Prompt regression",
            confidence=89,
            recommendation="Rollback v44",
            evidence=[],
        ),
        created_at=datetime.now(tz=timezone.utc),
    )
    assert incident.incident_id == "INC-001"
```

- [ ] **Step 2: Run tests to verify new tests fail**

```bash
pytest tests/test_schemas.py -v -k "trigger or rca or incident"
```

Expected: `ImportError` for `app.schemas.trigger` and `app.schemas.incident`

- [ ] **Step 3: Implement trigger schema**

Create `app/schemas/trigger.py`:

```python
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
```

- [ ] **Step 4: Implement incident schema**

Create `app/schemas/incident.py`:

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.trigger import TriggerReason


class RCAOutput(BaseModel):
    root_cause: str
    confidence: int  # 0-100
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
```

- [ ] **Step 5: Run all schema tests**

```bash
pytest tests/test_schemas.py -v
```

Expected: all 8 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add app/schemas/trigger.py app/schemas/incident.py tests/test_schemas.py
git commit -m "feat: add trigger and incident schemas with RCA output contract"
```

---

## Task 6: FastAPI App + API Stubs

**Files:**
- Create: `app/main.py`
- Create: `app/api/__init__.py`
- Create: `app/api/incidents.py`
- Create: `app/api/telemetry.py`
- Create: `app/api/metrics.py`
- Create: `app/api/simulation.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write failing API tests**

Create `tests/test_api.py`:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.anyio
async def test_get_incidents_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/incidents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_metrics_returns_dict():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "avg_latency_ms" in data
    assert "incident_count" in data


@pytest.mark.anyio
async def test_simulate_incident_accepts_scenario():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/simulate-incident", json={"scenario": "context_overflow"})
    assert response.status_code == 202


@pytest.mark.anyio
async def test_get_incident_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/incident/INC-999")
    assert response.status_code == 404
```

Create `tests/conftest.py`:

```python
import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_api.py -v
```

Expected: `ModuleNotFoundError: No module named 'app.main'`

- [ ] **Step 3: Create API route stubs**

Create `app/api/__init__.py` (empty).

Create `app/api/incidents.py`:

```python
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
```

Create `app/api/telemetry.py`:

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

router = APIRouter()


async def _event_stream():
    while True:
        yield f"data: {json.dumps({'status': 'streaming'})}\n\n"
        await asyncio.sleep(1)


@router.get("/telemetry/live")
async def live_telemetry():
    return StreamingResponse(_event_stream(), media_type="text/event-stream")
```

Create `app/api/metrics.py`:

```python
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
```

Create `app/api/simulation.py`:

```python
from fastapi import APIRouter
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
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Unknown scenario: {body.scenario}")
    return {"accepted": True, "scenario": body.scenario}
```

- [ ] **Step 4: Create main FastAPI app**

Create `app/main.py`:

```python
from fastapi import FastAPI
from app.api.incidents import router as incidents_router
from app.api.telemetry import router as telemetry_router
from app.api.metrics import router as metrics_router
from app.api.simulation import router as simulation_router

app = FastAPI(
    title="Autonomous AgentOps Intelligence",
    description="Autonomous AI agent failure intelligence platform",
    version="0.1.0",
)

app.include_router(incidents_router)
app.include_router(telemetry_router)
app.include_router(metrics_router)
app.include_router(simulation_router)
```

- [ ] **Step 5: Run all tests**

```bash
pytest tests/test_api.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 6: Verify app starts**

```bash
uvicorn app.main:app --reload &
sleep 2
curl http://localhost:8000/incidents
curl http://localhost:8000/metrics
kill %1
```

Expected: `[]` and `{"avg_latency_ms":0,...}`

- [ ] **Step 7: Commit**

```bash
git add app/main.py app/api/ tests/test_api.py tests/conftest.py
git commit -m "feat: add fastapi app with stubbed api routes"
```

---

## Task 7: Module Stubs (ingestion, retrieval, trigger, agent)

**Files:**
- Create: `app/ingestion/__init__.py`
- Create: `app/ingestion/base.py`
- Create: `app/synthetic_data/__init__.py`
- Create: `app/synthetic_data/generator.py`
- Create: `app/synthetic_data/scenarios/__init__.py`
- Create: `app/retrieval/__init__.py`
- Create: `app/retrieval/hybrid_search.py`
- Create: `app/trigger_engine/__init__.py`
- Create: `app/trigger_engine/rules.py`
- Create: `app/trigger_engine/detector.py`
- Create: `app/agent/__init__.py`
- Create: `app/agent/rca_agent.py`
- Create: `app/prompts/__init__.py`
- Create: `app/prompts/rca_prompt.py`

- [ ] **Step 1: Create ingestion base**

Create `app/ingestion/__init__.py` (empty).

Create `app/ingestion/base.py`:

```python
from abc import ABC, abstractmethod
from typing import Any


class BaseIngestor(ABC):
    """Normalize a raw event, generate its embedding, and index into OpenSearch."""

    @abstractmethod
    async def ingest(self, event: dict[str, Any]) -> str:
        """Ingest one event. Returns the OpenSearch document ID."""
        ...
```

- [ ] **Step 2: Create synthetic data stubs**

Create `app/synthetic_data/__init__.py` (empty).

Create `app/synthetic_data/scenarios/__init__.py` (empty).

Create `app/synthetic_data/generator.py`:

```python
from typing import AsyncIterator


class TelemetryGenerator:
    """Streams synthetic events from registered scenario generators."""

    async def stream(self) -> AsyncIterator[dict]:
        """Yields synthetic telemetry events indefinitely."""
        raise NotImplementedError
```

- [ ] **Step 3: Create retrieval stub**

Create `app/retrieval/__init__.py` (empty).

Create `app/retrieval/hybrid_search.py`:

```python
from typing import Any


class HybridSearch:
    """BM25 + vector + freshness retrieval against OpenSearch."""

    async def search(
        self,
        service: str,
        incident_type: str,
        time_window_minutes: int = 15,
        top_k: int = 20,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError
```

- [ ] **Step 4: Create trigger engine stubs**

Create `app/trigger_engine/__init__.py` (empty).

Create `app/trigger_engine/rules.py`:

```python
from app.config.settings import settings

LATENCY_MULTIPLIER = settings.trigger_latency_multiplier
ERROR_RATE_THRESHOLD = settings.trigger_error_rate_threshold
RETRY_THRESHOLD = settings.trigger_retry_threshold
TOKEN_SPIKE_THRESHOLD = settings.trigger_token_spike_threshold

LATENCY_BASELINE_MS = 800  # normal baseline for claims-agent
```

Create `app/trigger_engine/detector.py`:

```python
from typing import Optional
from app.schemas.trigger import TriggerEvent


class TriggerDetector:
    """Evaluates incoming telemetry windows against threshold rules."""

    def evaluate(self, window: dict) -> Optional[TriggerEvent]:
        """Return a TriggerEvent if any rule fires, else None."""
        raise NotImplementedError
```

- [ ] **Step 5: Create RCA agent stub**

Create `app/agent/__init__.py` (empty).

Create `app/agent/rca_agent.py`:

```python
from app.schemas.incident import RCAOutput
from app.schemas.trigger import TriggerEvent


class RCAAgent:
    """Uses Ollama/Qwen3 to generate root cause analysis from evidence."""

    async def analyze(
        self,
        trigger: TriggerEvent,
        evidence: list[dict],
    ) -> RCAOutput:
        raise NotImplementedError
```

- [ ] **Step 6: Create prompts**

Create `app/prompts/__init__.py` (empty).

Create `app/prompts/rca_prompt.py`:

```python
RCA_SYSTEM_PROMPT = """You are an AI production incident analyst.
Given a trigger event and evidence from logs, traces, and messages, identify the root cause.
Be concise. Cite specific evidence. Output valid JSON only."""

RCA_USER_TEMPLATE = """Trigger: {trigger_reason} on service: {service}

Evidence:
{evidence_text}

Output JSON with this exact schema:
{{
  "root_cause": "<string>",
  "confidence": <0-100>,
  "recommendation": "<string>",
  "evidence": ["<cited item 1>", ...]
}}"""
```

- [ ] **Step 7: Import check — verify all modules importable**

```bash
python -c "
from app.config.settings import settings
from app.schemas.telemetry import CloudWatchLog, LangfuseTrace, HangfireLog, TeamsMessage, DeploymentEvent
from app.schemas.trigger import TriggerReason, TriggerEvent
from app.schemas.incident import RCAOutput, Incident
from app.ingestion.base import BaseIngestor
from app.retrieval.hybrid_search import HybridSearch
from app.trigger_engine.detector import TriggerDetector
from app.trigger_engine.rules import LATENCY_BASELINE_MS
from app.agent.rca_agent import RCAAgent
from app.prompts.rca_prompt import RCA_SYSTEM_PROMPT
print('All imports OK')
"
```

Expected: `All imports OK`

- [ ] **Step 8: Run full test suite**

```bash
pytest tests/ -v
```

Expected: all tests PASS (no failures, no import errors).

- [ ] **Step 9: Commit**

```bash
git add app/ingestion/ app/synthetic_data/ app/retrieval/ app/trigger_engine/ app/agent/ app/prompts/
git commit -m "feat: add module stubs for ingestion, retrieval, trigger, and rca agent"
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Task |
|---|---|
| Python 3.12 + FastAPI | Task 1, 6 |
| OpenSearch in Docker | Task 2 |
| Ollama + nomic-embed-text + qwen3 | Task 2 |
| CloudWatch, Langfuse, Hangfire, Teams, Deployment schemas | Task 4 |
| TriggerReason enum + TriggerEvent | Task 5 |
| RCAOutput + Incident contract | Task 5 |
| GET /incidents, GET /incident/{id} | Task 6 |
| GET /telemetry/live (SSE) | Task 6 |
| POST /simulate-incident (5 scenarios) | Task 6 |
| GET /metrics | Task 6 |
| BaseIngestor ABC | Task 7 |
| HybridSearch stub | Task 7 |
| TriggerDetector stub | Task 7 |
| RCAAgent stub | Task 7 |
| RCA prompt template | Task 7 |
| Trigger threshold constants from settings | Task 3, 7 |

All spec requirements covered.

**Placeholder scan:** No TBDs. All code blocks complete. All imports resolvable within this plan.

**Type consistency:** `TriggerReason` defined in Task 5 `trigger.py`, used in `incident.py` (same task) and `detector.py` (Task 7) — consistent. `RCAOutput` defined Task 5, used in `RCAAgent.analyze` return type (Task 7) — consistent.
