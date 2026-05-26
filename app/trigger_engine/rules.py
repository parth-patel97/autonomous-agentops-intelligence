from app.config.settings import settings

LATENCY_MULTIPLIER = settings.trigger_latency_multiplier
ERROR_RATE_THRESHOLD = settings.trigger_error_rate_threshold
RETRY_THRESHOLD = settings.trigger_retry_threshold
TOKEN_SPIKE_THRESHOLD = settings.trigger_token_spike_threshold

LATENCY_BASELINE_MS = 800
