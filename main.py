import asyncio
from core.lightning_bot import LightningBolt
from services.config_manager import ConfigManager

if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.load()

    lightning_bolt = LightningBolt(config_manager)
    asyncio.run(lightning_bolt.run())