from dataclasses import dataclass

@dataclass
class Device:
    name: str = ""
    address: str = ""
    char_uuid: str = ""