
class ProfilesManager:
    def __init__(self):
        self.__profiles: dict[str, dict] = {}
        self.__active_profile: str = None

    def get_profiles(self) -> dict:
        return self.__profiles

    def set_profiles(self, profiles: dict) -> None:
        self.__profiles = profiles

    def get_active_profile(self) -> str:
        return self.__active_profile

    def set_active_profile(self, name: str) -> None:
        self.__active_profile = name

    def delete_active_profile(self) -> None:
        del self.__profiles[self.__active_profile]

    def get_active_profile_steps(self) -> dict:
        return self.__profiles[self.__active_profile].get("steps", {})

    def set_active_profile_steps(self, content: dict) -> None:
        self.__profiles[self.__active_profile]["steps"] = content

    def create_profile(self, profile_name: str) -> None:
        profiles = self.list_profiles()
        assert profile_name not in profiles, "Profile already exist!"
        self.__profiles[profile_name] = {}

    def is_profile_active(self) -> bool:
        return bool(self.__active_profile)

    def get_profile_content(self, name: str) -> dict:
        return self.__profiles[name]

    def get_active_profile_content(self) -> dict:
        return self.__profiles[self.__active_profile]

    def delete_profile(self, name: str) -> None:
        del self.__profiles[name]

    def list_profiles(self) -> list:
        profiles = list(self.__profiles.keys())
        return sorted(profiles)

    def first_profile(self) -> str:
        try:
            profiles = self.list_profiles()
            first_profile = sorted(profiles)[0]
            self.__active_profile = first_profile
            return first_profile
        except:
            return

    def rename_profile(self, original_name: str, new_name: str) -> None:
        self.__profiles[new_name] = self.__profiles[original_name]
        del self.__profiles[original_name]
