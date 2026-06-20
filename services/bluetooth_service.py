from bleak import BleakClient, BleakScanner
from models.device import Device

class BluetoothService:
    def __init__(self):
        self._last_scan: dict[str, str] = {}

    async def get_name(self, address: str) -> str | None:
        if address not in self._last_scan:
            await self.scan()

        return self._last_scan.get(address)
        

    async def scan(self) -> list[Device]:
        devices = await BleakScanner.discover()
        results = []

        for d in devices:
            self._last_scan[d.address] = d.name

            results.append(Device(
                name=d.name or 'Unknown',
                address=d.address
            ))
        
        return results
    
    async def explore(self, address: str) -> dict | None:
        async with BleakClient(address) as client:
            services = {}

            for service in client.services:
                services[service.uuid] = [
                    {
                        "uuid": char.uuid,
                        "properties": char.properties
                    }
                    for char in service.characteristics
                ]

            return services
    
    async def get_uuid(self, address: str) -> str | None:
        async with BleakClient(address) as client:
            chars = (
                char
                for service in client.services
                for char in service.characteristics
                if 'write-without-response' in char.properties

            )

            result = next(chars, None)

        return result.uuid if result else None