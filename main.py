import io
import mss
import asyncio
import colorsys
from PIL import Image
from bleak import BleakClient
from colorthief import ColorThief

class LightningBolt:
    ADDRESS = "BE:16:A7:00:03:51"
    LED_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
    INTERVAL = 0.15
    MONITOR = 1

    def __init__(self):
        self.client = BleakClient(self.ADDRESS, timeout=20.0)
        self.prev_color = (-50, -50, -50)

    async def connect(self) -> None:
        await self.client.connect()

    async def disconnect(self) -> None:
        await self.client.disconnect()

    async def send_color(self, r:int, g:int, b: int) -> None:
        cmd = bytes([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x0a, 0xef])
        await self.client.write_gatt_char(self.LED_CHAR_UUID, cmd, response=False)

    def capture_color(self) -> tuple[int, int, int]:
        with mss.MSS() as sct:
            monitor = sct.monitors[self.MONITOR]
            width = monitor["width"]
            height = monitor["height"]

            region = {
                "top":    monitor["top"]  + int(height * 0.20),
                "left":   monitor["left"] + int(width * 0.20),
                "width":  int(width * 0.60),
                "height": int(height * 0.60),
            }
            
            img = sct.grab(region)
            pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            pil_img = pil_img.resize((150, 150))

            buffer = io.BytesIO()
            pil_img.save(buffer, format="PNG")
            buffer.seek(0)

            ct = ColorThief(buffer)
            r, g, b = ct.get_color(quality=1)
            r, g, b = self.boost_color(r, g, b)
            return r, g, b
        
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
    def color_changed(c1: tuple, c2, threshold: int = 15) -> bool:
        return sum(abs(a - b) for a, b in zip(c1, c2)) > threshold

    async def run(self) -> None:
        await self.connect()

        try:
            while True:
                r, g, b = self.capture_color()

                if self.color_changed((r, g, b), self.prev_color):
                    await self.send_color(r, g, b)
                    self.prev_color = (r, g, b)
                    print(f"Color → R={r:3} G={g:3} B={b:3}")

                await asyncio.sleep(self.INTERVAL)

        except KeyboardInterrupt:
            pass
        finally:
            await self.disconnect()

if __name__ == "__main__":
    lightnint_bolt = LightningBolt()
    asyncio.run(lightnint_bolt.run())