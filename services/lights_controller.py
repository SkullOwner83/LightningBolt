from bleak import BleakClient
from models.device import Device

class LightsController:
    def __init__(self, device: Device):
        self.device = device
    
    @property
    def is_connected(self) -> bool:
        return self.client is not None and self.client.is_connected

    async def connect(self) -> None:
        self.client = BleakClient(self.device.address)
        await self.client.connect()
        print(f"Connected to device '{self.device.name}'")

    async def disconnect(self) -> None:
        await self.client.disconnect()
        print(f"Device '{self.device.name}' is disconnected")

    async def set_color(self, r:int, g:int, b: int) -> None:
        command = bytes([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x0a, 0xef])
        await self.client.write_gatt_char(self.device.char_uuid, command, response=False)