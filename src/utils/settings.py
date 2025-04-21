
from customtkinter import CTkToplevel

from src.controllers.engine import Engine
from src.types.profile_struct import ProfileStruct
from src.utils.profiles_file import ProfilesFile
from src.utils.profiles_manager import ProfilesManager
from src.utils.steps_manager import StepsManager
from src.utils.utility_functions import UtilityFunctions


class Settings:
    def __init__(self) -> None:
        self.profiles_file = ProfilesFile(filename="profiles")
        self.profiles_manager = ProfilesManager()
        self.steps_manager = StepsManager()
        self.profiles_manager.profiles = self.profiles_file.load()
        self.engine = Engine()
        
    def save_profile_settings(self, profile: ProfileStruct) -> None:
        self.profiles_manager.active_profile_steps = profile.to_dict()
        self.profiles_file.update(self.profiles_manager.profiles)

    def close_window_and_reset_speed(self, master: CTkToplevel) -> None:
        self.engine.reset(wait_until_end=True)
        UtilityFunctions.close_window(master)
