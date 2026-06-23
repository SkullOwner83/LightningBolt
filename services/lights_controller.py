from bleak import BleakClient
from models.device import Device

class LightsController:
    RECONNECT_TIMEOUT = 10.0

    def __init__(self, device: Device):
        self.device = device
        self.client: BleakClient | None = None
    
    @property
    def is_connected(self) -> bool:
        return self.client is not None and self.client.is_connected

    async def connect(self) -> None:
        if self.is_connected: return
        self.client = BleakClient(self.device.address, timeout=self.RECONNECT_TIMEOUT)
        await self.client.connect()
        print(f"Connected to device '{self.device.name}'")

    async def disconnect(self) -> None:
        if not self.is_connected: return
        await self.client.disconnect()
        print(f"Device '{self.device.name}' is disconnected")

    async def ensure_connected(self) -> bool:
        if self.is_connected: 
            return True

        try:
            await self.connect()
            return True
        except Exception as e:
            print(f"Reconnect failed for '{self.device.name}': {e}")
            return False

    async def set_color(self, r:int, g:int, b: int) -> None:
        if not await self.ensure_connected(): return
        command = bytes([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x0a, 0xef])
        await self.client.write_gatt_char(self.device.char_uuid, command, response=False)