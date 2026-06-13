import asyncio
import colorsys
from lights_controller import LightsController
from screen_capture import ScreenCapture

class LightningBolt:
    ADDRESS = "BE:16:A7:00:03:51"
    LED_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
    INTERVAL = 0.15
    MONITOR = 1

    def __init__(self):
        self.screen = ScreenCapture(self.MONITOR)
        self.lights = LightsController(self.ADDRESS, self.LED_CHAR_UUID)
        self.prev_color: tuple[int,int,int] | None = None

    @staticmethod
    def boost_color(r: int, g: int, b: int) -> tuple[int, int, int]:
        r /= 255
        g /= 255
        b /= 255

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # subir saturación y controlar brillo
        s = min(1, s * 1.8)
        v = min(1, v * 1.1)

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r*255), int(g*255), int(b*255)

    @staticmethod
    def color_changed(color1: tuple, color2: tuple, threshold: int = 15) -> bool:
        if color1 or color2 == None: return True
        return sum(abs(a - b) for a, b in zip(color1, color2)) > threshold

    async def run(self) -> None:
        try:
            await self.lights.connect()

            while True:
                r, g, b = self.screen.capture_color()
                r, g, b = self.boost_color(r, g, b)

                if self.color_changed((r, g, b), self.prev_color):
                    await self.lights.set_color(r, g, b)
                    self.prev_color = (r, g, b)
                    print(f"Color → R={r:3} G={g:3} B={b:3}")

                await asyncio.sleep(self.INTERVAL)
        except KeyboardInterrupt:
            print("Deteniendo programa...")
        finally:
            await self.lights.disconnect()

if __name__ == "__main__":
    lightning_bolt = LightningBolt()
    asyncio.run(lightning_bolt.run())