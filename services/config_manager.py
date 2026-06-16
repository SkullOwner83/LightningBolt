import os
import json
from pathlib import Path
from models.device import Device

class ConfigManager:
    CONFIG_PATH = Path(os.getenv('LOCALAPPDATA')) / "LightningBolt" / "settings.json"

    def __init__(self):
        self._devices: dict[str, Device] = {}
        self.load() 

    @property
    def devices(self) -> dict[str, Device]:
        return self._devices.copy()

    def load(self, path: Path = None) -> None:
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
        

    def save(self, path: Path = None) -> None:
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
        self._devices[device.key] = device
        self.save()

    def remove_device(self, key: str):
        self._devices.pop(key, None)
        self.save()