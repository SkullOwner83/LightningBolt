import uuid
from fastapi import APIRouter, HTTPException, Request, status
from models.device import Device
from services.bluetooth_service import BluetoothService
from services.config_manager import ConfigManager

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_devices(request: Request):
    config: ConfigManager = request.app.state.config
    devices = list(config.devices.values())
    return devices

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_device(payload: Device, request: Request):
    config: ConfigManager = request.app.state.config
    bluetooth: BluetoothService = request.app.state.bluetooth
    char_uuid = await bluetooth.explore(payload.address)

    if not char_uuid:
        raise HTTPException(status_code=400, detail="No se encontró característica escribible.")

    device = Device(
        key=str(uuid.uuid4()),
        name=payload.name,
        address=payload.address,
        char_uuid=char_uuid
    )

    config.add_device(device)

@router.delete("/{key}", status_code=status.HTTP_200_OK)
async def remove_device(key: str, request: Request):
    config: ConfigManager = request.app.state.config
    config.remove_device(key)

@router.get("/scan", status_code=status.HTTP_200_OK)
async def scan_devices(request: Request):
    scanner: BluetoothService = request.app.state.bluetooth
    devices = await scanner.scan()
    return devices