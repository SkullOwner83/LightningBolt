import uuid
from fastapi import APIRouter, HTTPException, Request, status
from core.lightning_bot import LightningBolt
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
    bolt: LightningBolt = request.app.state.bolt
    config: ConfigManager = request.app.state.config
    bluetooth: BluetoothService = request.app.state.bluetooth

    if any(d.address == payload.address for d in config.devices.values()):
        raise HTTPException(status_code=409, detail=f"Device with address '{payload.address}' already exists")
    
    key = await bluetooth.get_name(payload.address)
    char_uuid = await bluetooth.get_uuid(payload.address)

    if key is None:
        raise HTTPException(status_code=404, detail="Device not found")

    if not char_uuid:
        raise HTTPException(status_code=400, detail="Not founded writable feature or device is not support.")

    device = Device(
        id=str(uuid.uuid4()),
        key=key,
        name=payload.name,
        address=payload.address,
        char_uuid=char_uuid
    )

    try:
        config.add_device(device)
    except ValueError as ex:
        raise HTTPException(status_code=409, detail=str(ex))

    try:
        await bolt.add_light(device)
    except Exception as ex:
        config.remove_device(device.id)
        raise HTTPException(status_code=400, detail=f"Could not connect: {ex}")

    return device

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def remove_device(id: str, request: Request):
    bolt: LightningBolt = request.app.state.bolt
    config: ConfigManager = request.app.state.config

    try:
        await bolt.remove_light(id)
        config.remove_device(id)
    except ValueError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.get("/scan", status_code=status.HTTP_200_OK)
async def scan_devices(request: Request):
    scanner: BluetoothService = request.app.state.bluetooth
    devices = await scanner.scan()
    return devices

@router.get("/explore", status_code=status.HTTP_200_OK)
async def explore_devices(address: str, request: Request):
    scanner: BluetoothService = request.app.state.bluetooth
    services = await scanner.explore(address)
    return services
