from datetime import timedelta
from typing import TypedDict

from axis_direction import AxisDirection


class ProfileFile(TypedDict):
    speed: int
    time: timedelta
    direction: AxisDirection
