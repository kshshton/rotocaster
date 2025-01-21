from customtkinter import CTkToplevel

from src.controllers.engine import Engine
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
        self.engine = Engine()

    def save_profile_settings(self, profile: ProfileStruct) -> None:
        self.profiles_manager.active_profile_steps = profile.to_dict()
        self.file.update(self.profiles_manager.profiles)

    def close_window_and_reset_speed(self, master: CTkToplevel) -> None:
        self.engine.operation(SpeedOperator.DECREMENT)
        UtilityFunctions.close_window(master)
