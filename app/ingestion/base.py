from abc import ABC, abstractmethod
from typing import Any


class BaseIngestor(ABC):
    @abstractmethod
    async def ingest(self, event: dict[str, Any]) -> str:
        ...
