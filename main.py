import asyncio
import mss
from PIL import Image
from bleak import BleakClient

# === CONFIGURACIÓN ===
ADDRESS       = "BE:16:A7:00:03:51"
LED_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
INTERVAL      = 0.15  # segundos entre capturas

def build_color_command(r, g, b):
    return bytes([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x0a, 0xef])

from colorthief import ColorThief
import io

async def get_screen_color():
    with mss.MSS() as sct:
        monitor = sct.monitors[1]
        # Captura el centro (60% de la pantalla)
        w = monitor["width"]
        h = monitor["height"]
        region = {
            "top":    monitor["top"]  + int(h * 0.20),
            "left":   monitor["left"] + int(w * 0.20),
            "width":  int(w * 0.60),
            "height": int(h * 0.60),
        }
        img = sct.grab(region)
        pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        pil_img = pil_img.resize((150, 150))

        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        buffer.seek(0)

        ct = ColorThief(buffer)
        r, g, b = ct.get_color(quality=1)
        r, g, b = boost_color(r, g, b)
        return r, g, b

import colorsys

def boost_color(r, g, b):
    r /= 255
    g /= 255
    b /= 255

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # subir saturación y controlar brillo
    s = min(1, s * 1.8)
    v = min(1, v * 1.1)

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return int(r*255), int(g*255), int(b*255)

async def main():
    print("Conectando... (asegúrate que Magic Lantern esté cerrado)")
    async with BleakClient(ADDRESS, timeout=20.0) as client:
        print("✅ Conectado. Modo ambiente activado — Ctrl+C para salir.\n")
        prev_color = (-50, -50, -50)

        while True:
            try:
                r, g, b = await get_screen_color()
                diff = sum(abs(a - b2) for a, b2 in zip((r, g, b), prev_color))
                if diff > 15:
                    cmd = build_color_command(r, g, b)
                    await client.write_gatt_char(LED_CHAR_UUID, cmd, response=False)
                    prev_color = (r, g, b)
                    print(f"Color → R={r:3} G={g:3} B={b:3}")
                await asyncio.sleep(INTERVAL)

            except KeyboardInterrupt:
                print("\n👋 Saliendo...")
                break

asyncio.run(main())