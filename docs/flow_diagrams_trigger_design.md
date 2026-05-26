
# Flow Diagrams & Trigger Design
# Autonomous AI Agent Failure Intelligence Platform

## 1. High-Level End-to-End Flow

```text
Synthetic Event Generators
(CloudWatch / Langfuse / Hangfire / Teams / Deployment)
                        │
                        ▼
                Event Ingestion Layer
             (normalization + embedding)
                        │
                        ▼
                  OpenSearch Storage
       keyword + vector + metadata indexing
                        │
                        ▼
                  Trigger Engine
      (threshold detection / anomaly rules)
                        │
              incident trigger event
                        ▼
               Retrieval Orchestrator
      BM25 + Vector + Freshness Ranking
                        │
                        ▼
                   Evidence Bundle
                        │
                        ▼
                     RCA Agent
          (reasoning + recommendation)
                        │
                        ▼
                Incident JSON Output
                        │
                        ▼
                  Dashboard Update
```

---

## 2. Trigger Flow

System is autonomous.

NO USER INPUT.

### Trigger Sequence

```text
Telemetry arrives
      │
      ▼
Metrics computed
(error rate / retries / latency)
      │
      ▼
Threshold crossed?
      │
 ┌────┴────┐
 │   NO    │
 │ continue│
 └─────────┘
      │
     YES
      │
      ▼
Generate incident event
      │
      ▼
Run retrieval pipeline
      │
      ▼
Run RCA agent
      │
      ▼
Dashboard incident card
```

---

## 3. Example Incident Flow

### Scenario:
Prompt Regression

```text
09:55 deployment v44
      │
      ▼
10:00 latency spike
      │
      ▼
10:01 Langfuse failures
      │
      ▼
10:02 Hangfire retries spike
      │
      ▼
10:03 Teams discussion
("Did prompt change?")
      │
      ▼
Trigger engine fires
      │
      ▼
Retrieve evidence
      │
      ▼
RCA generated
```

---

## 4. Trigger Engine Flow

### Inputs

Input Streams:

1. CloudWatch logs
2. Langfuse traces
3. Hangfire failures
4. Teams messages
5. deployment events

### Logic

```text
Incoming Event
      │
      ▼
Extract Metrics
      │
      ▼
Check Rules
      │
      ├── latency > threshold
      ├── failure rate > threshold
      ├── retry spike
      ├── token spike
      └── error spike
              │
              ▼
       Create Incident Trigger
```

### Example Rule

```python
if latency > baseline * 3:
    trigger()

if retry_count > threshold:
    trigger()

if failure_rate > threshold:
    trigger()
```

---

## 5. Retrieval Flow

Once trigger fires:

```text
Trigger Event
      │
      ▼
Build Search Query
(service + incident type + time)
      │
      ▼
Keyword Search (BM25)
      │
      ▼
Vector Search
      │
      ▼
Metadata Filter
(last 15 mins + service)
      │
      ▼
Freshness Ranking
      │
      ▼
Top Evidence Bundle
```

### Input

```json
{
  "service":"claims-agent",
  "incident_type":"latency_spike",
  "time_window":"15m"
}
```

### Output

```json
{
  "evidence":[
    "deployment v44",
    "context_length_exceeded",
    "retry failures",
    "teams discussion"
  ]
}
```

---

## 6. RCA Agent Flow

```text
Evidence Bundle
      │
      ▼
Prompt Builder
      │
      ▼
LLM Reasoning
      │
      ▼
Root Cause
Confidence
Recommendation
Evidence
      │
      ▼
Incident JSON
```

### RCA Input

```json
{
 "trigger_reason":"latency_spike",
 "evidence":[]
}
```

### RCA Output

```json
{
 "incident_id":"INC-001",
 "root_cause":"Prompt regression",
 "confidence":91,
 "recommendation":"Rollback v44",
 "evidence":[]
}
```

---

## 7. Full Input → Output Example

### Input

CloudWatch

```json
{
 "message":"context_length_exceeded",
 "service":"claims-agent"
}
```

Langfuse

```json
{
 "latency_ms":4200,
 "prompt_version":"v44"
}
```

Hangfire

```json
{
 "retry_count":5
}
```

Teams

```json
{
 "message":"Seeing failures after rollout"
}
```

### System Trigger

```json
{
 "incident_id":"INC-001",
 "reason":"latency_spike"
}
```

### Final Output

```json
{
 "incident_id":"INC-001",
 "root_cause":"Prompt regression",
 "confidence":89,
 "recommendation":"Rollback v44",
 "evidence":[
   "deployment v44",
   "latency increase",
   "retry storm",
   "teams discussion"
 ]
}
```

---

## 8. Sequence Diagram

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
        ├── no issue → continue streaming
        │
        └── anomaly detected
                    │
                    ▼
          Retrieval Orchestrator
                    │
                    ▼
               RCA Agent
                    │
                    ▼
             Incident Output
                    │
                    ▼
                Dashboard
```

---

## 9. Dashboard Data Flow

```text
Incident JSON
      │
      ▼
Frontend API
      │
      ▼
Incident Cards
RCA Summary
Evidence Timeline
Metrics Panel
```

---

## 10. Lifecycle of One Incident

```text
Deployment event
      ↓
Failure logs appear
      ↓
Latency spikes
      ↓
Threshold crossed
      ↓
Trigger fires
      ↓
Retrieve evidence
      ↓
Generate RCA
      ↓
Dashboard update
      ↓
Incident archived
```

---

## 11. Why RAG Exists Here

Without RAG:

```text
all logs + traces + chats
      ↓
massive context
      ↓
expensive LLM
```

With RAG:

```text
retrieve only relevant evidence
      ↓
small context
      ↓
cheaper + faster + better RCA
```
