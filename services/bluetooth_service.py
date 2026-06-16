from bleak import BleakClient, BleakScanner
from models.device import Device

class BluetoothService:
    async def scan(self) -> list[Device]:
        devices = await BleakScanner.discover()

        return [
            Device(
                name=d.name or "Unknown", 
                address=d.address
            )
            for d in devices
        ]
    
    async def explore(self, address: str) -> str | None:
        async with BleakClient(address) as client:
            char = (
                char
                for service in client.services
                for char in service.characteristics
                if 'write-without-response' in char.properties

            )

        return next(char, None)