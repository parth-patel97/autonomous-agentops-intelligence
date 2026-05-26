from typing import Optional
from app.schemas.trigger import TriggerEvent


class TriggerDetector:
    def evaluate(self, window: dict) -> Optional[TriggerEvent]:
        raise NotImplementedError
