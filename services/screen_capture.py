import io
import mss
from PIL import Image
from colorthief import ColorThief

class ScreenCapture:
    def __init__(self, monitor: int = 1):
        self.sct = mss.MSS()
        self.monitor = self.sct.monitors[monitor]

    def capture_color(self) -> tuple[int, int, int] | None:
        monitor = self.monitor
        width = monitor["width"]
        height = monitor["height"]

        region = {
            "top":    monitor["top"]  + int(height * 0.20),
            "left":   monitor["left"] + int(width * 0.20),
            "width":  int(width * 0.60),
            "height": int(height * 0.60),
        }
        
        try:
            img = self.sct.grab(region)
            image = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            image = image.resize((150, 150))

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            ct = ColorThief(buffer)
        
            r, g, b = ct.get_color(quality=1)
            return r, g, b
        except Exception:
            return None