from customtkinter import CTkToplevel

from src.controllers.speed_suspension import SpeedSuspension
from src.types.profile_struct import ProfileStruct
from src.types.speed_operator import SpeedOperator
from src.utils.profiles_file import ProfilesFile
from src.utils.profiles_manager import ProfilesManager
from src.utils.steps_manager import StepsManager
from src.utils.utility_functions import UtilityFunctions


class Settings:
    def __init__(self) -> None:
        self.file = ProfilesFile(filename="profiles")
        self.profiles_manager = ProfilesManager()
        self.steps_manager = StepsManager()
        self.profiles_manager.profiles = self.file.load()
        self.suspension = SpeedSuspension()

    def save_profile_settings(self, value: ProfileStruct) -> None:
        self.profiles_manager.active_profile_content = value.to_dict()
        self.file.update(self.profiles_manager.profiles)

    def close_window_and_reset_speed(self, master: CTkToplevel) -> None:
        self.suspension.operation(SpeedOperator.DECREMENT)
        UtilityFunctions.close_window(master)
