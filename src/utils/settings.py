from typing import Optional

from customtkinter import CTkToplevel

from src.controllers.speed_damper import SpeedDamper
from src.types.profile_struct import ProfileStruct
from src.types.speed_operator import SpeedOperator
from src.utils.profiles_file import ProfilesFile
from src.utils.profiles_manager import ProfilesManager


class Settings:
    def __init__(self) -> None:
        self.file = ProfilesFile(filename="profiles")
        self.manager = ProfilesManager()
        self.manager.profiles = self.file.load()
        self.damper = SpeedDamper()

    def close_window(
        self,
        window: CTkToplevel,
        callback: Optional[callable] = None
    ) -> None:
        self.damper.speed_operation(SpeedOperator.DECREMENT)
        try:
            callback()
        except TypeError:
            pass
        finally:
            window.destroy()

    def save_window_settings(self, master: any, value: ProfileStruct) -> None:
        self.manager.active_profile_content = value.to_dict()
        self.file.update(self.manager.profiles)
        self.close_window(master)
