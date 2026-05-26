# Requirements.md
# Autonomous AI Agent Failure Intelligence Platform using Real-Time RAG

## 1. Project Overview

### Objective
Build an autonomous, trigger-based, real-time RAG platform that monitors synthetic telemetry from:
- Microsoft Teams
- AWS CloudWatch logs
- Langfuse traces/model calls
- Hangfire background job logs

The system automatically detects anomalies, retrieves relevant evidence using hybrid retrieval, generates RCA (root cause analysis), and surfaces incident summaries in a dashboard.

No user chat interaction is required.

### Positioning
This project demonstrates:

- Real-time RAG
- Event-driven system design
- Autonomous AI reasoning
- Hybrid retrieval (BM25 + embeddings)
- Production-style observability patterns
- AgentOps debugging and RCA automation
- Cost optimization via retrieval instead of brute-force prompting

## 2. Problem Statement

Modern AI agents are difficult to debug in production.

Teams often investigate failures across:
- CloudWatch logs
- Langfuse model traces
- Hangfire job failures
- Teams discussions
- deployment events

The process is manual, slow, expensive, and fragmented.

This system autonomously:
1. Detects anomalies
2. Triggers investigation
3. Retrieves relevant context
4. Generates RCA
5. Displays evidence and recommendation

## 3. Goals

### Functional Goals
- Real-time telemetry simulation
- Automatic incident detection
- Autonomous trigger-based RCA
- Real-time hybrid RAG retrieval
- Incident dashboard
- Historical incident matching

### Non Goals
- Production deployment
- Authentication
- RBAC
- Multi-tenant architecture
- Human chat interface

## 4. Architecture

```text
Synthetic Generators
 (CloudWatch/Langfuse/Hangfire/Teams)
                ↓
        Event Ingestion Layer
                ↓
           OpenSearch
        (keyword + vector)
                ↓
          Trigger Engine
                ↓
          Retrieval Engine
     BM25 + Vector + Freshness
                ↓
             RCA Agent
                ↓
         Incident Dashboard
```

## 5. Recommended Tech Stack

Backend:
- Python 3.12
- FastAPI

Search:
- OpenSearch (local docker)

Embeddings:
- Ollama
- nomic-embed-text OR bge-m3

LLM:
- Ollama
- Qwen

Frontend:
- Next.js OR Streamlit

Storage:
- OpenSearch only for MVP

## 6. Folder Structure

```text
project/
├── app/
│   ├── api/
│   ├── agent/
│   ├── retrieval/
│   ├── ingestion/
│   ├── trigger_engine/
│   ├── synthetic_data/
│   ├── schemas/
│   ├── prompts/
│   └── config/
├── dashboard/
├── evaluation/
├── docs/
├── requirements.md
└── docker-compose.yml
```

## 7. Synthetic Data Requirements

Create realistic telemetry generators.

### CloudWatch Logs
Fields:
- timestamp
- service
- severity
- message
- trace_id
- deployment_id

Example:
```json
{
  "timestamp": "2026-01-01T10:00:00Z",
  "service": "claims-agent",
  "severity": "ERROR",
  "message": "context_length_exceeded",
  "trace_id": "abc123"
}
```

### Langfuse Traces
Fields:
- trace_id
- prompt_version
- latency
- token_usage
- model
- status

### Hangfire Logs
Fields:
- job_id
- queue
- retry_count
- status
- error_message

### Teams Messages
Fields:
- sender
- timestamp
- message
- channel

### Deployment Events
Fields:
- service
- version
- deployed_at

## 8. Incident Scenarios

Implement at least 5 scenarios.

1. Prompt regression
2. Context overflow
3. Retry storm
4. Model latency spike
5. Cost explosion

Each scenario should emit correlated telemetry.

## 9. OpenSearch Design

Indexes:
- cloudwatch_logs
- langfuse_traces
- hangfire_logs
- teams_messages
- incidents

Required:
- vector fields
- timestamp filtering
- metadata filtering
- BM25 search

## 10. Trigger Engine

Rule-based trigger only.

Example:

```python
if (
    error_rate > threshold
    or latency > threshold
):
    trigger_rca()
```

Trigger Conditions:
- latency spike
- retry spike
- failure spike
- cost spike

## 11. Retrieval Strategy

Use hybrid retrieval:

1. BM25 keyword search
2. Semantic vector retrieval
3. Freshness ranking

Formula:

final_score =
semantic_score +
keyword_score +
freshness_weight

Time filter:
Last 15 minutes

Retrieve:
Top 20 evidence items

## 12. RCA Agent

Input:
- retrieved evidence
- historical incidents
- deployment metadata

Output:
- root cause
- confidence score
- evidence list
- recommendation

Example output:

Incident ID: INC-001

Root Cause:
Prompt version regression

Confidence:
89%

Evidence:
- deployment change
- Langfuse latency increase
- Hangfire failures
- Teams discussion

Recommendation:
Rollback prompt version

## 13. APIs

GET /incidents
GET /incident/{id}
GET /telemetry/live
POST /simulate-incident
GET /metrics

## 14. Dashboard Requirements

Sections:
1. Live telemetry feed
2. Triggered incidents
3. AI RCA panel
4. Evidence timeline
5. Langfuse metrics
6. Hangfire failures

## 15. Evaluation Metrics

Measure:
- retrieval precision
- latency
- token reduction
- hallucination reduction
- incident detection accuracy

## 16. RAG vs No-RAG Comparison

Without RAG:
- large context
- high latency
- expensive inference
- noisy reasoning

With RAG:
- smaller context
- cheaper
- faster
- better signal

## 17. Milestones

Phase 1:
Synthetic generators

Phase 2:
OpenSearch ingestion

Phase 3:
Hybrid retrieval

Phase 4:
Trigger engine

Phase 5:
RCA agent

Phase 6:
Dashboard

Phase 7:
Evaluation

## 18. Acceptance Criteria

System must:
- auto trigger incidents
- generate RCA
- retrieve evidence
- display dashboard
- support real-time updates

## 19. Demo Flow

1. Start telemetry stream
2. Trigger synthetic incident
3. Observe trigger firing
4. Observe retrieval
5. Observe RCA generation
6. View dashboard evidence

## 20. Future Enhancements

- Redis Streams
- Multi-agent orchestration
- Slack/Teams notifications
- Auto-remediation
- LangGraph orchestration
