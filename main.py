import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.lightning_bot import LightningBolt
from services.config_manager import ConfigManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ConfigManager()
    config.load()

    bolt = LightningBolt(config)
    app.state.bolt = bolt
    asyncio.create_task(bolt.run())
    yield


app = FastAPI(title="LightningBolt", version="1.0.0", lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=45678)