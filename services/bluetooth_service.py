from bleak import BleakClient, BleakScanner
from models.device import Device

class BluetoothService:
    async def scan(self) -> list[Device]:
        devices = await BleakScanner.discover()

        return [
            Device(
                name=d.name or "Desconocido", 
                address=d.address
            )
            for d in devices
            #if d.name
        ]
    
    async def explorer(self, address: str) -> dict:
        services = {}

        async with BleakClient(address) as client:
            for service in client.services:
                services[service.uuid] = [
                    {
                        "uuid": char.uuid,
                        "properties": char.properties
                    }
                    for char in service.characteristics
                ]

        return services