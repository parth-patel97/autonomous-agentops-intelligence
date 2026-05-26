
# Autonomous AI Agent Failure Intelligence Platform
## Full Implementation Requirements (Implementation-Ready)

## 1. Vision

Build an autonomous, trigger-based real-time RAG system for AI production incident intelligence.

The platform continuously observes synthetic telemetry inspired by real production systems:

- Microsoft Teams discussions
- AWS CloudWatch logs
- Langfuse traces/model calls
- Hangfire job failures
- deployment events

The system automatically:

1. Detects anomalies
2. Triggers investigation
3. Retrieves evidence using hybrid retrieval
4. Generates root cause analysis (RCA)
5. Produces recommendations
6. Updates dashboard

No human prompt/chat interface is required.

---

## 2. Architecture

```text
Synthetic Data Generators
(cloudwatch/langfuse/hangfire/teams/deployments)
                    ↓
            Ingestion Service
                    ↓
               OpenSearch
        keyword + vector indexes
                    ↓
             Trigger Engine
         (threshold/anomaly rules)
                    ↓
           Retrieval Orchestrator
BM25 + vector + metadata + freshness
                    ↓
                RCA Agent
                    ↓
             Incident Store
                    ↓
               Dashboard UI
```

---

## 3. Tech Stack

Backend
- Python 3.12
- FastAPI
- asyncio

Search & Retrieval
- OpenSearch (Docker)

Embedding
- Ollama
- nomic-embed-text

LLM
- Ollama + Qwen3

Frontend
- Next.js (preferred)

Optional
- Redis Streams later

Do NOT use:
- CrewAI
- heavy LangChain abstractions

---

## 4. Repository Structure

```text
project/
│
├── app/
│   ├── api/
│   │   ├── incidents.py
│   │   ├── telemetry.py
│   │   └── metrics.py
│   │
│   ├── ingestion/
│   │   ├── cloudwatch_ingestor.py
│   │   ├── langfuse_ingestor.py
│   │   ├── hangfire_ingestor.py
│   │   └── teams_ingestor.py
│   │
│   ├── synthetic_data/
│   │   ├── generator.py
│   │   ├── scenarios/
│   │   └── templates/
│   │
│   ├── retrieval/
│   │   ├── hybrid_search.py
│   │   ├── reranker.py
│   │   └── freshness.py
│   │
│   ├── trigger_engine/
│   │   ├── rules.py
│   │   └── detector.py
│   │
│   ├── agent/
│   │   ├── rca_agent.py
│   │   ├── evidence_builder.py
│   │   └── incident_generator.py
│   │
│   ├── prompts/
│   ├── schemas/
│   └── config/
│
├── dashboard/
├── docs/
├── tests/
└── docker-compose.yml
```

---

## 5. Synthetic Telemetry

Generate realistic event streams.

### CloudWatch Logs Schema

```json
{
  "timestamp":"2026-05-26T10:00:00Z",
  "service":"claims-agent",
  "severity":"ERROR",
  "message":"context_length_exceeded",
  "trace_id":"trace-123",
  "deployment_id":"dep-33",
  "environment":"prod"
}
```

### Langfuse Schema

```json
{
  "trace_id":"trace-123",
  "prompt_version":"v44",
  "latency_ms":4100,
  "token_input":23000,
  "token_output":1200,
  "model":"qwen",
  "status":"failure",
  "cost":0.02
}
```

### Hangfire Schema

```json
{
  "job_id":"job-11",
  "queue":"claims",
  "retry_count":4,
  "status":"failed",
  "error_message":"context_length_exceeded"
}
```

### Teams Schema

```json
{
  "sender":"Ali",
  "channel":"ai-prod",
  "timestamp":"2026-05-26T10:05:00Z",
  "message":"Seeing latency spike after prompt deploy"
}
```

### Deployment Schema

```json
{
  "deployment_id":"dep-33",
  "service":"claims-agent",
  "version":"v44",
  "deployed_at":"2026-05-26T09:55:00Z"
}
```

---

## 6. Incident Scenarios

Create 5 deterministic scenarios.

### Scenario 1: Prompt Regression
Symptoms:
- latency spike
- failures increase
- Teams discussion references rollout

### Scenario 2: Context Overflow
Symptoms:
- context_length_exceeded
- Hangfire retries spike

### Scenario 3: Retry Storm
Symptoms:
- repeated failures
- queue saturation

### Scenario 4: Cost Explosion
Symptoms:
- Langfuse token usage spikes

### Scenario 5: Model Latency Spike
Symptoms:
- response delay increases 4x baseline

---

## 7. OpenSearch Design

Indexes:

- cloudwatch_logs
- langfuse_traces
- hangfire_logs
- teams_messages
- deployments
- incidents

Required fields:
- timestamp
- service
- metadata
- embedding
- incident_id

Mapping example:

```json
{
 "properties": {
   "message":{"type":"text"},
   "service":{"type":"keyword"},
   "timestamp":{"type":"date"},
   "embedding":{
      "type":"knn_vector",
      "dimension":768
   }
 }
}
```

---

## 8. Trigger Engine

Rule-based only.

Pseudo logic:

```python
if error_rate > threshold:
    trigger()

if latency > baseline * 3:
    trigger()

if retry_count > threshold:
    trigger()
```

Trigger output:

```json
{
 "incident_id":"INC-001",
 "service":"claims-agent",
 "trigger_reason":"latency_spike"
}
```

---

## 9. Retrieval Design

Use hybrid retrieval.

Score:

```text
final_score =
0.4 * keyword_score +
0.4 * semantic_score +
0.2 * freshness_score
```

Retrieve:

- top 20 evidence items
- last 15 minutes priority
- service filter required

Evidence sources:
- logs
- traces
- jobs
- teams
- deployments
- historical incidents

---

## 10. RCA Agent

Inputs:
- evidence bundle
- trigger reason
- historical incidents

Prompt strategy:

1. summarize evidence
2. identify probable cause
3. generate confidence
4. cite evidence
5. recommend action

Output contract:

```json
{
 "root_cause":"Prompt regression",
 "confidence":89,
 "recommendation":"Rollback v44",
 "evidence":[]
}
```

---

## 11. API Contracts

### GET /incidents

Returns all incidents.

### GET /incident/{id}

Returns:
- RCA
- evidence
- timeline

### POST /simulate-incident

Body:

```json
{
 "scenario":"context_overflow"
}
```

### GET /telemetry/live

Returns streaming events.

### GET /metrics

Returns:
- avg_latency
- incident_count
- retrieval_time
- token_reduction

---

## 12. Dashboard

Sections:

1. Live telemetry feed
2. Incident cards
3. RCA panel
4. Evidence timeline
5. Langfuse metrics
6. Hangfire failures

Suggested layout:

```text
------------------------------------------------
Live Feed | Incident Feed
------------------------------------------------
RCA Summary
------------------------------------------------
Evidence Timeline
------------------------------------------------
Metrics
------------------------------------------------
```

---

## 13. Evaluation

Measure:

- retrieval precision
- hallucination rate
- avg RCA latency
- token reduction
- retrieval latency

Compare:

No RAG vs RAG

Metrics:
- token cost
- latency
- accuracy

---

## 14. Demo Flow

1. start stack
2. stream telemetry
3. trigger scenario
4. anomaly fires
5. retrieval runs
6. RCA generated
7. dashboard updates

---

## 15. Milestones

Week 1
- generators
- OpenSearch
- ingestion

Week 2
- trigger engine
- retrieval

Week 3
- RCA agent
- dashboard

Week 4
- evaluation
- polish

---

## 16. Acceptance Criteria

Must:
- auto-trigger incidents
- no human interaction
- hybrid retrieval works
- RCA generated automatically
- dashboard updated live
- synthetic scenarios reproducible

---

## 17. Local Setup

Docker:
- OpenSearch
- OpenSearch dashboard
- Ollama

Commands:

```bash
docker compose up -d
ollama pull qwen3
ollama pull nomic-embed-text
```

Run:

```bash
uvicorn app.main:app --reload
```

---

## 18. Coding Guidance for AI Agents

Implement in order:

1. synthetic generators
2. ingestion
3. OpenSearch indexes
4. trigger engine
5. retrieval
6. RCA agent
7. dashboard
8. evaluation

Never implement chat UI.

Prioritize deterministic demos.
