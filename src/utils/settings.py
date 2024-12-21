from typing import Optional

from customtkinter import CTkToplevel

from src.profiles.profiles_file import ProfilesFile
from src.profiles.profiles_manager import ProfilesManager
from src.speed.speed_damper import SpeedDamper
from src.speed.speed_operator import SpeedOperator


class Settings:
    def __init__(self) -> None:
        self._file = ProfilesFile(filename="profiles")
        self._manager = ProfilesManager()
        self._manager.profiles = self._file.load()
        self._damper = SpeedDamper()

    def _close_window(
        self,
        window: CTkToplevel,
        callback: Optional[callable] = None
    ) -> None:
        self._damper.speed_operation(SpeedOperator.DECREMENT)
        try:
            callback()
        except TypeError:
            pass
        finally:
            window.destroy()

    def _save_profile(self, master: any, value: int) -> None:
        self._manager.active_profile_value = value
        self._file.update(self._manager.profiles)
        self._close_window(master)
