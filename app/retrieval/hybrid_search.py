from typing import Any


class HybridSearch:
    async def search(
        self,
        service: str,
        incident_type: str,
        time_window_minutes: int = 15,
        top_k: int = 20,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError
