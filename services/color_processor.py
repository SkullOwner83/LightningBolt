import colorsys

class ColorProcessor:
    def __init__(self):
        pass

    def boost_color(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        r /= 255
        g /= 255
        b /= 255

        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        s = min(1, s * 1.8)
        v = min(1, v * 1.1)

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)
    
    def color_changed(self, color1: tuple, color2: tuple | None, threshold: int = 15) -> bool:
        if color2 is None: 
            return True
        
        diference = sum(abs(a - b) for a, b in zip(color1, color2))
        return diference > threshold