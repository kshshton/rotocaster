from typing import Optional

from customtkinter import CTkToplevel

from src.types.profile_struct import ProfileStruct
from src.types.speed_operator import SpeedOperator
from src.utils.profiles_file import ProfilesFile
from src.utils.profiles_manager import ProfilesManager
from src.utils.speed_damper import SpeedDamper


class Settings:
    def __init__(self) -> None:
        self._file = ProfilesFile(filename="profiles")
        self._manager = ProfilesManager()
        self._manager.profiles = self._file.load()
        self._damper = SpeedDamper()

    def close_window(
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

    def save_window_settings(self, master: any, value: ProfileStruct) -> None:
        self._manager.active_profile_content = value.to_dict()
        self._file.update(self._manager.profiles)
        self.close_window(master)
