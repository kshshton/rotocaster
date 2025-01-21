
class ProfilesManager:
    def __init__(self):
        self.__profiles: dict[str, dict] = {}
        self.__active_profile: str = None

    @property
    def profiles(self) -> dict:
        return self.__profiles

    @profiles.setter
    def profiles(self, profiles: dict) -> None:
        self.__profiles = profiles

    @property
    def active_profile(self) -> None:
        return self.__active_profile

    @active_profile.setter
    def active_profile(self, name: str) -> None:
        self.__active_profile = name

    @active_profile.deleter
    def active_profile(self) -> None:
        if len(self.list_profiles()) == 1:
            self.create_profile("")
        del self.__profiles[self.active_profile]

    @property
    def active_profile_steps(self) -> dict:
        return self.__profiles[self.active_profile].get("steps", {})

    @active_profile_steps.setter
    def active_profile_steps(self, content: dict) -> None:
        self.__profiles[self.active_profile]["steps"] = content

    def create_profile(self, profile_name: str) -> None:
        profiles = self.list_profiles()
        if profile_name in profiles:
            return
        if "" in self.list_profiles():
            self.delete_profile("")
        self.__profiles[profile_name] = {}

    def is_profile_active(self) -> bool:
        return bool(self.active_profile)

    def get_profile(self, name: str) -> dict:
        return self.__profiles[name]

    def get_active_profile(self) -> dict:
        return self.__profiles[self.active_profile]

    def delete_profile(self, name: str) -> None:
        del self.__profiles[name]

    def select_profile(self, name: str) -> None:
        self.active_profile = name

    def list_profiles(self) -> list:
        try:
            profiles = list(self.__profiles.keys())
            if len(profiles) > 1 and "" in profiles:
                del self.__profiles[""]
            return sorted(profiles)
        except:
            return []

    def first_profile(self) -> str:
        profiles = self.list_profiles()
        first_profile = next(iter(profiles), "")
        self.active_profile = first_profile
        return first_profile

    def update_steps_for_profile(self, profile_name: str, steps: dict) -> None:
        profile = self.profiles[profile_name]
        profile["steps"] = steps

    def rename_profile(self, original_name: str, new_name: str) -> None:
        self.__profiles[new_name] = self.__profiles[original_name]
        del self.__profiles[original_name]

