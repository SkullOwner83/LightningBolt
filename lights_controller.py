from bleak import BleakClient

class LightsController:
    def __init__(self, address: str, uuid: str):
        self.address = address
        self.uuid = uuid
        self.client = None
    
    async def connect(self) -> None:
        self.client = BleakClient(self.address)
        await self.client.connect()
        print("Connected to device")

    async def disconnect(self) -> None:
        await self.client.disconnect()
        print("Device is disconnected")

    async def set_color(self, r:int, g:int, b: int) -> None:
        command = bytes([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x0a, 0xef])
        await self.client.write_gatt_char(self.uuid, command, response=False)