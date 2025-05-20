from src.controllers.engine import Engine
from src.utils.profiles_file import ProfilesFile
from src.utils.profiles_manager import ProfilesManager
from src.utils.steps_manager import StepsManager


class Context:
    def __init__(self) -> None:
        self.profiles_file = ProfilesFile(filename="profiles")
        self.profiles_manager = ProfilesManager()
        self.steps_manager = StepsManager()
        self.profiles_manager.set_profiles(self.profiles_file.load())
        self.engine = Engine()

    def save_profile_context(self, profile_content: dict) -> None:
        active_profile = self.profiles_manager.get_active_profile_name()
        self.profiles_manager.set_profile_steps(
            active_profile, profile_content)
        self.profiles_file.update(self.profiles_manager.get_profiles())
