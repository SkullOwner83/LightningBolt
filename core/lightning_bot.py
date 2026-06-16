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
        self.colors = ColorProcessor()
        self.prev_color: tuple[int,int,int] | None = None
        
        self.lights: list[LightsController] = [
            LightsController(device)
            for device in config_manager.devices.values()
        ]

    async def connect_lights(self) -> None:
        await asyncio.gather(*[light.connect() for light in self.lights])

    async def set_color_all(self, r: int, g: int , b: int) -> None:
        await asyncio.gather(*[light.set_color(r, g, b) for light in self.lights])

    async def run(self) -> None:
        try:
            await self.connect_lights()

            while True:
                r, g, b = await asyncio.to_thread(self.screen.capture_color)
                r, g, b = self.colors.boost_color(r, g, b)

                if self.colors.color_changed((r, g, b), self.prev_color):
                    await self.set_color_all(r, g, b)
                    self.prev_color = (r, g, b)
                    print(f"Color → R={r:3} G={g:3} B={b:3}")

                await asyncio.sleep(self.INTERVAL)
        except KeyboardInterrupt:
            print("Stoping program...")
        finally:
            for light in self.lights:
                await light.disconnect()