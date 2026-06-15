from fastapi import APIRouter, Request
from services.bluetooth_service import BluetoothService

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)

@router.get("/scan")
async def scan_devices():
    scanner = BluetoothService()
    devices = await scanner.scan()
    return devices

@router.get("/explore")
async def explore(address: str):
    explorer = BluetoothService()
    services = await explorer.explorer(address)
    return services