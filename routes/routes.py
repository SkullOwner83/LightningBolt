from fastapi import APIRouter, Request
from core.lightning_bot import LightningBolt

router = APIRouter()

@router.get("/status")
async def status(request: Request):
    bolt: LightningBolt = request.app.state.bolt

    return {
        "status": bolt.lights.is_connected,
        "previous color": bolt.prev_color
    }
