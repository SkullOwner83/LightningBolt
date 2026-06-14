import asyncio
from services.lights_controller import LightsController
from services.screen_capture import ScreenCapture
from services.color_processor import ColorProcessor
from services.config_manager import ConfigManager

class LightningBolt:
    INTERVAL = 0.15
    MONITOR = 1

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.screen = ScreenCapture(self.MONITOR)
        self.lights = LightsController(self.config_manager.device)
        self.colors = ColorProcessor()
        self.prev_color: tuple[int,int,int] | None = None

    async def run(self) -> None:
        try:
            await self.lights.connect()

            while True:
                r, g, b = await asyncio.to_thread(self.screen.capture_color)
                r, g, b = self.colors.boost_color(r, g, b)

                if self.colors.color_changed((r, g, b), self.prev_color):
                    await self.lights.set_color(r, g, b)
                    self.prev_color = (r, g, b)
                    print(f"Color → R={r:3} G={g:3} B={b:3}")

                await asyncio.sleep(self.INTERVAL)
        except KeyboardInterrupt:
            print("Deteniendo programa...")
        finally:
            await self.lights.disconnect()