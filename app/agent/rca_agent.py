from app.schemas.incident import RCAOutput
from app.schemas.trigger import TriggerEvent


class RCAAgent:
    async def analyze(self, trigger: TriggerEvent, evidence: list[dict]) -> RCAOutput:
        raise NotImplementedError
