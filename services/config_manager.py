import os
import json
from pathlib import Path
from models.device import Device

class ConfigManager:
    CONFIG_PATH = Path(os.getenv('LOCALAPPDATA')) / "LightningBolt" / "settings.json"

    def __init__(self):
        self._devices: dict[str, Device] = {}

    @property
    def devices(self) -> dict[str, Device]:
        return self._devices.copy()

    def load(self, path: Path | None = None) -> None:
        path = self.CONFIG_PATH if path is None else path

        if not path.exists():
            self._devices = {}
            self.save()
            return

        with open(path, "r") as file:
            try:
                data: dict = json.load(file)

                self._devices = {
                    k: Device(**v) 
                    for k, v in data.get("devices",  {}).items()
                }
            except json.JSONDecodeError:
                raise ValueError("The file is not a valid format")
        

    def save(self, path: Path | None = None) -> None:
        path = self.CONFIG_PATH if path is None else path
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "devices": { 
                key: device.to_dict() 
                for key, device in self.devices.items() 
            }
        }

        with open(path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_device(self, device: Device):
        if any(d.address == device.address for d in self.devices.values()):
            raise ValueError(f"Device with the address '{device.address}' already exists")

        self._devices[device.id] = device
        self.save()

    def remove_device(self, id: str):
        if id not in self._devices:
            raise ValueError("Device not found")

        self._devices.pop(id, None)
        self.save()