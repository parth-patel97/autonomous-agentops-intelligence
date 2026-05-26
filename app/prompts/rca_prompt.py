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
