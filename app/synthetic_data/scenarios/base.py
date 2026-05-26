from abc import ABC, abstractmethod


class BaseScenario(ABC):
    name: str
    service: str = "claims-agent"

    @abstractmethod
    def generate(self) -> list[dict]:
        """Return correlated telemetry events. Each dict has '_source_type' key."""
        ...

    def _wrap(self, source_type: str, model_instance) -> dict:
        return {"_source_type": source_type, **model_instance.model_dump(mode="json")}
