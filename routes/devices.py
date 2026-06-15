from fastapi import APIRouter, Request, status
from core.lightning_bot import LightningBolt
from models.device import Device
from services.bluetooth_service import BluetoothService
from services.config_manager import ConfigManager

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)

@router.get("/scan", status_code=status.HTTP_200_OK)
async def scan_devices():
    scanner = BluetoothService()
    devices = await scanner.scan()
    return devices

@router.get("/explore", status_code=status.HTTP_200_OK)
async def explore(address: str):
    explorer = BluetoothService()
    services = await explorer.explorer(address)
    return services

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_device(device: Device, request: Request):
    config: ConfigManager = request.app.state.config
    bolt: LightningBolt = request.app.state.bolt
    config.add_device(device)