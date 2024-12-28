from dataclasses import dataclass
from datetime import timedelta
from typing import Union


@dataclass
class ProfileStruct:
    speed: int
    time: timedelta
    direction: str

    def to_dict(self) -> dict[str, Union[int, timedelta, str]]:
        return {
            "speed": self.speed, 
            "time": self.time, 
            "direction": self.direction
        }
