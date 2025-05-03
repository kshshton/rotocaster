
class ProfilesManager:
    def __init__(self):
        self.__profiles: dict[str, dict] = {}
        self.__active_profile_name: str = None

    def get_profiles(self) -> dict:
        return self.__profiles

    def set_profiles(self, profiles: dict) -> None:
        self.__profiles = profiles

    def get_active_profile_name(self) -> str:
        return self.__active_profile_name

    def set_active_profile_name(self, name: str) -> None:
        assert name is not None, "Name is empty!"
        self.__active_profile_name = name

    def create_profile(self, profile_name: str) -> None:
        profiles = self.list_profiles()
        assert profile_name not in profiles, "Profile already exist!"
        self.__profiles[profile_name] = {}

    def is_profile_active(self) -> bool:
        return bool(self.__active_profile_name)

    def get_profile_steps(self, name: str) -> dict:
        return self.__profiles[name]["steps"]

    def set_profile_steps(self, name: str, steps: dict) -> None:
        self.__profiles[name]["steps"] = steps

    def get_active_profile_steps(self) -> dict:
        return self.__profiles[self.__active_profile_name]["steps"]

    def set_active_profile_steps(self, steps: dict) -> None:
        self.__profiles[self.__active_profile_name]["steps"] = steps

    def delete_profile(self, name: str) -> None:
        del self.__profiles[name]

    def delete_active_profile(self) -> None:
        del self.__profiles[self.__active_profile_name]

    def list_profiles(self) -> list:
        profiles = list(self.__profiles.keys())
        return sorted(profiles)

    def first_profile(self) -> str:
        try:
            profiles = self.list_profiles()
            return profiles[0]
        except:
            return

    def rename_profile(self, original_name: str, new_name: str) -> None:
        self.__profiles[new_name] = self.__profiles[original_name]
        del self.__profiles[original_name]
