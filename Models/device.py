from dataclasses import asdict, dataclass

@dataclass
class Device:
    key: str = ""
    name: str = ""
    address: str = ""
    char_uuid: str = ""

    def to_dict(self) -> dict:
        return asdict(self)