from typing import AsyncIterator


class TelemetryGenerator:
    async def stream(self) -> AsyncIterator[dict]:
        raise NotImplementedError
