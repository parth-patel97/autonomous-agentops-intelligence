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
