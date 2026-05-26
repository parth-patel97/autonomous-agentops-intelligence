
# Architecture Diagrams
# Autonomous AI Agent Failure Intelligence Platform

## 1. High-Level System Architecture

```text
┌──────────────────────────────────────────────┐
│         Synthetic Event Generators           │
│----------------------------------------------│
│ CloudWatch Logs                              │
│ Langfuse Model Calls                         │
│ Hangfire Job Logs                            │
│ Teams Messages                               │
│ Deployment Events                            │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│              Ingestion Layer                 │
│----------------------------------------------│
│ Normalize Payload                            │
│ Generate Embeddings                          │
│ Add Metadata                                 │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│                OpenSearch                    │
│----------------------------------------------│
│ Keyword Index (BM25)                         │
│ Vector Index                                 │
│ Metadata Filtering                           │
│ Time-based Search                            │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│               Trigger Engine                 │
│----------------------------------------------│
│ Error Spike Detection                        │
│ Retry Spike Detection                        │
│ Latency Spike Detection                      │
│ Cost Spike Detection                         │
└──────────────────────────────────────────────┘
                      │
              Incident Trigger
                      ▼
┌──────────────────────────────────────────────┐
│          Retrieval Orchestrator              │
│----------------------------------------------│
│ BM25 Retrieval                               │
│ Semantic Retrieval                           │
│ Freshness Ranking                            │
│ Evidence Bundle Builder                      │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│                  RCA Agent                   │
│----------------------------------------------│
│ Root Cause Analysis                          │
│ Confidence Score                             │
│ Recommendation                               │
│ Evidence Citation                            │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│                Dashboard UI                  │
│----------------------------------------------│
│ Incident Cards                               │
│ Live Feed                                    │
│ RCA Panel                                    │
│ Metrics                                      │
│ Evidence Timeline                            │
└──────────────────────────────────────────────┘
```

---

## 2. Trigger Decision Tree

```text
Incoming Telemetry Event
            │
            ▼
     Calculate Metrics
            │
            ▼
     Check Trigger Rules
            │
    ┌───────┼────────┬───────────┐
    │       │        │           │
    ▼       ▼        ▼           ▼
Latency  Failure   Retry      Token
Spike    Spike     Spike      Spike
    │       │        │           │
    └───────┴────────┴───────────┘
                    │
                    ▼
           Create Incident Trigger
                    │
                    ▼
               Start Retrieval
```

---

## 3. Sequence Diagram

```text
Synthetic Generator
        │
        ▼
Ingestion Service
        │
        ▼
OpenSearch
        │
        ▼
Trigger Engine
        │
        ├── No anomaly
        │        │
        │        ▼
        │    Continue Streaming
        │
        └── Trigger Detected
                 │
                 ▼
      Retrieval Orchestrator
                 │
                 ▼
            RCA Agent
                 │
                 ▼
          Incident JSON
                 │
                 ▼
            Dashboard
```

---

## 4. Retrieval Pipeline Diagram

```text
Incident Trigger
       │
       ▼
Build Retrieval Query
(service + incident + timeframe)
       │
       ▼
┌───────────────────────────┐
│      BM25 Retrieval       │
│ keyword match             │
└───────────────────────────┘
       │
       ▼
┌───────────────────────────┐
│    Semantic Retrieval     │
│ embedding similarity      │
└───────────────────────────┘
       │
       ▼
┌───────────────────────────┐
│ Metadata Filtering        │
│ service + timestamp       │
└───────────────────────────┘
       │
       ▼
┌───────────────────────────┐
│ Freshness Ranking         │
│ prioritize recent events  │
└───────────────────────────┘
       │
       ▼
Evidence Bundle
```

---

## 5. Data Flow Diagram

```text
Telemetry
  │
  ├── CloudWatch Logs
  ├── Langfuse Traces
  ├── Hangfire Logs
  ├── Teams Messages
  └── Deployments
          │
          ▼
   Normalize + Embed
          │
          ▼
      OpenSearch
          │
          ▼
      Trigger Engine
          │
          ▼
        Retrieval
          │
          ▼
         RCA
          │
          ▼
      Incident Store
          │
          ▼
       Dashboard
```

---

## 6. Incident Lifecycle

```text
Deployment
    │
    ▼
Telemetry Spike
    │
    ▼
Anomaly Detection
    │
    ▼
Trigger Fired
    │
    ▼
Evidence Retrieval
    │
    ▼
RCA Generated
    │
    ▼
Dashboard Updated
    │
    ▼
Incident Archived
```

---

## 7. Input → Output Flow

### Input

```json
{
  "service":"claims-agent",
  "latency_ms":4200,
  "retry_count":5,
  "message":"context_length_exceeded"
}
```

### Internal Flow

```text
Trigger Engine
      │
      ▼
Retrieval Query
      │
      ▼
Evidence Bundle
      │
      ▼
RCA Agent
```

### Output

```json
{
  "incident_id":"INC-001",
  "root_cause":"Prompt regression",
  "confidence":91,
  "recommendation":"Rollback v44"
}
```

---

## 8. Dashboard Wireframe

```text
┌────────────────────────────────────────────┐
│ Live Telemetry Feed                        │
├────────────────────────────────────────────┤
│ Triggered Incidents                        │
├────────────────────────────────────────────┤
│ RCA Summary                                │
├────────────────────────────────────────────┤
│ Evidence Timeline                          │
├────────────────────────────────────────────┤
│ Metrics                                    │
└────────────────────────────────────────────┘
```

---

## 9. Deployment Architecture (Local)

```text
Docker
 │
 ├── OpenSearch
 ├── OpenSearch Dashboard
 ├── Ollama
 └── FastAPI Backend
             │
             ▼
         Next.js UI
```

---

## 10. Why Real-Time RAG

```text
Without RAG
all telemetry
      │
      ▼
 huge context
      │
 expensive + noisy
      ▼
 weak RCA

With RAG
retrieve relevant evidence
      │
      ▼
 small context
      │
 cheaper + faster
      ▼
 stronger RCA
```
