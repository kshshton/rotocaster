from src.controllers.speed_suspension import SpeedSuspension
from src.types.profile_struct import ProfileStruct
from src.utils.profiles_file import ProfilesFile
from src.utils.profiles_manager import ProfilesManager
from src.utils.utility_functions import UtilityFunctions


class Settings:
    def __init__(self) -> None:
        self.file = ProfilesFile(filename="profiles")
        self.manager = ProfilesManager()
        self.manager.profiles = self.file.load()
        self.suspension = SpeedSuspension()

    def save_window_settings(self, master: any, value: ProfileStruct) -> None:
        self.manager.active_profile_content = value.to_dict()
        self.file.update(self.manager.profiles)
        UtilityFunctions.close_window(master)
