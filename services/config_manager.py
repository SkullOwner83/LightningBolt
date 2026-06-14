import os
import json
from pathlib import Path
from types import SimpleNamespace
from models.device import Device

class ConfigManager:
    CONFIG_PATH = Path(os.getenv('LOCALAPPDATA')) / "LightningBolt" / "settings.json"

    def __init__(self):
        self.device = Device()
        self.load() 

    def load(self, path: Path = None) -> None:
        path = self.CONFIG_PATH if path is None else path

        if not path.exists():
            self.save(self.device.__dict__)

        with open(path, "r") as file:
            try:
                stored_config = json.load(file)
                self.device = SimpleNamespace(**stored_config)
            except json.JSONDecodeError:
                raise ValueError("The file is not a valid format")

    def save(self, data: dict,  path: Path = None) -> None:
        path = self.CONFIG_PATH if path is None else path
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)