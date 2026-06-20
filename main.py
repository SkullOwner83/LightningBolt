import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.lightning_bot import LightningBolt
from services.bluetooth_service import BluetoothService
from services.config_manager import ConfigManager
from routes import devices, routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ConfigManager()
    config.load()

    bolt = LightningBolt(config)
    bluetooth = BluetoothService()
    task = asyncio.create_task(bolt.run())
    app.state.bolt = bolt
    app.state.config = config
    app.state.bluetooth = bluetooth
    
    yield
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="LightningBolt", version="1.0.0", lifespan=lifespan)
app.include_router(devices.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=45678)