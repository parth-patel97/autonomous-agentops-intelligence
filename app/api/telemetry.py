import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


async def _event_stream():
    while True:
        yield f"data: {json.dumps({'status': 'streaming'})}\n\n"
        await asyncio.sleep(1)


@router.get("/telemetry/live")
async def live_telemetry():
    return StreamingResponse(_event_stream(), media_type="text/event-stream")
