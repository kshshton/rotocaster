from dataclasses import dataclass, field
from datetime import timedelta
from typing import Union


@dataclass
class ProfileStruct:
    speed: int
    time: timedelta
    direction: str
    steps: dict[str, dict] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Union[int, str, dict]]:
        return {
            "speed": self.speed, 
            "time": self.time, 
            "direction": self.direction,
            "steps": self.steps,
        }
